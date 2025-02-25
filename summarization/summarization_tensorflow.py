from datasets import load_dataset, concatenate_datasets, DatasetDict
from transformers import(
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    TFAutoModelForSeq2SeqLM,
    pipeline,
    create_optimizer
)
from transformers.keras_callbacks import PushToHubCallback
import tensorflow as tf
import evaluate
import numpy as np
import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize


class Summarization(object):
    def __init__(self):
        self.model =None
        self.raw_data_en = None
        self.raw_data_sp = None
        self.collection_dataset = None
        self.data_collator = None
        self.model_checkpoint = None
        self.tokenizer = None
        self.tokenized_dataset = None
        self.args = None
        self.metric = None
        self.max_input_length = 512
        self.max_target_length = 30
        self.other_name = None

    def load_dataset(self, name1="defunct-datasets/amazon_reviews_multi", name2="defunct-datasets/amazon_reviews_multi" ):
        self.raw_data_en = load_dataset(name1, data_dir="en", revision="refs/convert/parquet")
        self.raw_data_sp= load_dataset(name2,data_dir="es" ,revision="refs/convert/parquet")
        print("Name of dataset1: ", name1)
        print(self.raw_data_en)
        print("Name of dataset2: ", name2)
        print(self.raw_data_sp)

    def load_support(self, name="google/mt5-small"):
        self.model_checkpoint = name
        self.other_name = self.model_checkpoint.split("/")[-1]
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_checkpoint, return_tensor="tf")
        print("Name of model checkpoint: ", self.model_checkpoint)
        print("Other name: ", self.other_name)
        print("Tokenizer Fast: ", self.tokenizer.is_fast)
        print("Model max length tokenizer: ", self.tokenizer.model_max_length)

    def create_model(self):
        print("Start creating model")
        self.model = TFAutoModelForSeq2SeqLM.from_pretrained(self.model_checkpoint)
        print(self.model)

    def create_collator(self):
        self.data_collator = DataCollatorForSeq2Seq(tokenizer=self.tokenizer, model=self.model, return_tensors="tf")
        
    def get_feature_items(self, raw_data, set="train", index=0, feature="review_body"):
        return raw_data[set][index][feature]
    
    def get_pair_feature(self, raw_data, set="train", index=0, feature1="review_body", feature2="review_title"):
        line1 = self.get_feature_items(raw_data, set, index, feature1)
        line2 = self.get_feature_items(raw_data, set, index, feature2)
        return line1, line2
    
    def explore_dataset(self, type="en", set='train', index=None, feature="product_category"):
        if type == "en":
            raw_data = self.raw_data_en
            raw_data.set_format("pandas")
        else:
            raw_data = self.raw_data_sp
            raw_data.set_format("pandas")
        df_raw_data = raw_data[set][:]
        print(df_raw_data[feature].value_counts()[:20])


    def filter_dataset(self, example):
        feature = "product_category"
        type1 = "book"
        type2 = "digital_ebook_purchase"
        return (example[feature] == type1 or example[feature] == type2)
    
    def map_filter_dataset(self):
        self.raw_data_en.reset_format()
        self.raw_data_sp.reset_format()
        print("Start mapping filter dataset")
        self.raw_data_en = self.raw_data_en.filter(self.filter_dataset)
        self.raw_data_sp = self.raw_data_sp.filter(self.filter_dataset)
        print("Done mapping filter dataset")
        print(self.raw_data_en)
        print("\n")
        print(self.raw_data_sp)

    def concatenate_dataset(self):
        self.collection_dataset = DatasetDict()
        print(self.raw_data_en.keys())
        for split in self.raw_data_en.keys():
            self.collection_dataset[split] = concatenate_datasets(
                [self.raw_data_en[split], self.raw_data_sp[split]]
            )
            self.collection_dataset[split] = self.collection_dataset[split].shuffle(seed=42)
        '''Distribution of length of text is not formal => FILTER length > 2'''
        feature = "review_title"
        self.collection_dataset = self.collection_dataset.filter(lambda x: len(x[feature].split()) > 2)
        print("New collection dataset: ", self.collection_dataset)

    def tokenize_dataset(self, example):
        feature1 = "review_body"
        feature2= "review_title"
        '''Tokenize for INPUTS'''
        model_inputs = self.tokenizer(example[feature1], max_length=self.max_input_length, truncation=True)
        '''Tokenize for TARGETS in context'''
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(example[feature2], max_length=self.max_target_length, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    def map_tokenize_dataset(self):
        self.tokenized_dataset = self.collection_dataset.map(
            self.tokenize_dataset,
            batched=True,
            remove_columns=self.collection_dataset["train"].column_names
        )
        print("Tokenized dataset for training: ", self.tokenized_dataset)
    
    def convert_tf_type(self, batch_size=64):
        self.train_dataset = self.tokenized_dataset["train"].to_tf_dataset(
            columns=["input_ids", "attention_mask", "labels"],
            collate_fn=self.data_collator,
            shuffle=True,
            batch_size=batch_size,
        )
        self.val_dataset = self.tokenized_dataset["validation"].to_tf_dataset(
            columns=["input_ids", "attention_mask", "labels"],
            collate_fn=self.data_collator,
            shuffle=False,
            batch_size=batch_size,
        )

    def create_metric(self, name="rouge"):
        self.metric = evaluate.load(name)

    def compute_metrics(self, eval_prediction):
        predictions, labels = eval_prediction
        '''Decode LOGIT of prediction to TEXT'''
        decoded_predictions = self.tokenizer.batch_decode(predictions, skip_special_tokens=True)

        '''Bacause LABEL use [-100] for padding NOT SAME MODEL pad_token_id => convert to [PAD]'''
        labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id)
        decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True) 

        '''ROUGE need each line for evaluate => Add '\n' each new line'''  
        decoded_predictions = ["\n".join(sent_tokenize(prediction.strip())) for prediction in decoded_predictions]
        decoded_labels = ["\n".join(sent_tokenize(label.strip())) for label in decoded_labels]            

        result = self.metric.compute(predictions=decoded_predictions, labels=decoded_labels)
        result = {key: value * 100 for key, value in result.items()}
        return {k: round(v, 4) for k, v in result.items()}
    
    def  create_hyperparameter(self, learning_rate=5.6e-5, weight_decay=0.01,
                              num_warmup_steps=0, num_train_epochs=20):
        self.epochs = num_train_epochs
        num_train_steps = len(self.train_dataset)*self.epochs
        self.optimizer, self.scheduler = create_optimizer(
            init_lr=learning_rate,
            num_warmup_steps=num_warmup_steps,
            num_train_steps=num_train_steps,
            weight_decay_rate=weight_decay,
        )
        print("Optimizer ready for training")
        return self.optimizer, self.scheduler
    
    def call_train(self, output_dir="TF_fine_tuned_", save_strategy="epoch",push_to_hub=False,
                    save_local=False, hub_model_id="", checkpoint=False):
        if push_to_hub:
            output_dir = output_dir + self.other_name
            callback = PushToHubCallback(output_dir=output_dir , save_strategy=save_strategy,
                                                            tokenizer=self.tokenizer, hub_model_id=hub_model_id, checkpoint=checkpoint)
        else:
            callback = None
        self.model.compile(optimizer=self.optimizer)
        #tf.keras.mixed_precision.set_global_policy("mixed_float16")
        #print("Basis evaluation before of training: ", self.model.evaluate(self.val_dataset))

        self.model.fit(
            self.train_dataset,
            validation_data=self.val_dataset,
            callbacks=[callback],
            epochs=self.epochs,
        )
        print("Done training")
        print("Done pushing push to hub")

        print("Basis evaluation after of training: ", self.model.evaluate(self.val_dataset))

    def call_pipeline(self, local=False, path="", example=""):
        if local:
            model_checkpoint = ""
        else:
            model_checkpoint = path
        summary = pipeline(
            "summarization",
            model=model_checkpoint,
        )
        print("Summary: ",summary(example)[0]["summary_text"])
    
    def test(self, index):
        review = self.tokenized_dataset["test"][index]["review_body"]
        title = self.tokenized_dataset["test"][index]["review_title"]
        print(f"'>>> Review: {review}'")
        print(f"\n'>>> Title: {title}'")
        self.call_pipeline(path="Chessmen/TF_fine_tuned_"+ self.other_name, example= review)

if __name__ == "__main__":
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    1_LOADING DATASET
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    print("-"*50, "Exploring information of Supporting", "-"*50)
    summary = Summarization()
    summary.load_dataset()
    print("-"*50, "Exploring information of Supporting", "-"*50)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    2_EXPLORING DATASET, 
      _CREATING MODEL
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    print("-"*50, "Exploring information of Supporting", "-"*50)
    summary.load_support()
    summary.create_model()
    summary.create_collator()
    summary.create_metric()
    print("-"*50, "Exploring information of Supporting", "-"*50)
    print("Example[0] (text) in dataset: ", summary.get_feature_items(summary.raw_data_en, set="train", index=0, feature="review_body"))
    print("Example[0] (label) in dataset: ", summary.get_feature_items(summary.raw_data_en, set="train", index=0, feature="review_title"))
    print("\n")
    line1, line2 = summary.get_pair_feature(summary.raw_data_en, set="train", index=1, feature1="review_body", feature2="review_title")
    print("--> Inp of Example[1] in English: ", line1)
    print("--> Out of Example[1] in English: ", line2)
    print("\n")
    line1, line2 = summary.get_pair_feature(summary.raw_data_sp,set="train", index=1, feature1="review_body", feature2="review_title")
    print("--> Inp of Example[1] in Spanish: ", line1)
    print("--> Out of Example[1] in Spanish: ", line2)
    print("\n")
    print("Show top 20 information as table in English: ")
    summary.explore_dataset(type="en", set='train', index=None, feature="product_category")
    print("\n")
    print("Show top 20 information as table in Spanish: ")
    summary.explore_dataset(type="sp", set='train', index=None, feature="product_category")

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    3_PRE-PROCESSING DATASET, 
      _COMPUTE METRICS
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    summary.map_filter_dataset()
    summary.concatenate_dataset()
    summary.map_tokenize_dataset()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    4_SELECTION HYPERPARMETERS
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    summary.create_hyperparameter(num_train_epochs=10, push_to_hub=True, hub_model_id="Chessmen/"+"TF_fine_tune_" + summary.other_name)
    summary.call_train(save_local=True,push_to_hub=True)
    

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        5_USE PRE-TRAINED MODEL
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    summary.call_pipeline(path="Chessmen/TF_fine_tune_mt5-small", example= "Muy apropiado para mis hijas")
    summary.test(index=100)