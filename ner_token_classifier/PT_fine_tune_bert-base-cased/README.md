---
library_name: transformers
license: apache-2.0
base_model: bert-base-cased
tags:
- generated_from_trainer
metrics:
- precision
- recall
- f1
- accuracy
model-index:
- name: fine_tune_bert-base-cased
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# fine_tune_bert-base-cased

This model is a fine-tuned version of [bert-base-cased](https://huggingface.co/bert-base-cased) on an unknown dataset.
It achieves the following results on the evaluation set:
- Loss: 0.0842
- Precision: 0.9376
- Recall: 0.9541
- F1: 0.9458
- Accuracy: 0.9866

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 64
- eval_batch_size: 64
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 20

### Training results

| Training Loss | Epoch | Step | Validation Loss | Precision | Recall | F1     | Accuracy |
|:-------------:|:-----:|:----:|:---------------:|:---------:|:------:|:------:|:--------:|
| 0.2667        | 1.0   | 220  | 0.0739          | 0.8619    | 0.9118 | 0.8862 | 0.9776   |
| 0.0602        | 2.0   | 440  | 0.0641          | 0.9109    | 0.9357 | 0.9231 | 0.9830   |
| 0.0361        | 3.0   | 660  | 0.0594          | 0.9187    | 0.9401 | 0.9293 | 0.9845   |
| 0.0234        | 4.0   | 880  | 0.0564          | 0.9233    | 0.9461 | 0.9346 | 0.9854   |
| 0.0164        | 5.0   | 1100 | 0.0585          | 0.9211    | 0.9465 | 0.9336 | 0.9856   |
| 0.0123        | 6.0   | 1320 | 0.0656          | 0.9212    | 0.9483 | 0.9346 | 0.9850   |
| 0.0084        | 7.0   | 1540 | 0.0639          | 0.9290    | 0.9514 | 0.9401 | 0.9864   |
| 0.0072        | 8.0   | 1760 | 0.0735          | 0.9325    | 0.9482 | 0.9403 | 0.9862   |
| 0.0051        | 9.0   | 1980 | 0.0745          | 0.9319    | 0.9488 | 0.9403 | 0.9856   |
| 0.0042        | 10.0  | 2200 | 0.0783          | 0.9308    | 0.9490 | 0.9398 | 0.9858   |
| 0.0034        | 11.0  | 2420 | 0.0782          | 0.9337    | 0.9509 | 0.9422 | 0.9862   |
| 0.0026        | 12.0  | 2640 | 0.0822          | 0.9328    | 0.9505 | 0.9416 | 0.9858   |
| 0.0019        | 13.0  | 2860 | 0.0785          | 0.9335    | 0.9525 | 0.9429 | 0.9862   |
| 0.0018        | 14.0  | 3080 | 0.0819          | 0.9382    | 0.9525 | 0.9453 | 0.9865   |
| 0.0015        | 15.0  | 3300 | 0.0846          | 0.9349    | 0.9524 | 0.9436 | 0.9863   |
| 0.0013        | 16.0  | 3520 | 0.0880          | 0.9353    | 0.9519 | 0.9435 | 0.9860   |
| 0.0012        | 17.0  | 3740 | 0.0846          | 0.9362    | 0.9527 | 0.9444 | 0.9864   |
| 0.001         | 18.0  | 3960 | 0.0868          | 0.9374    | 0.9532 | 0.9453 | 0.9864   |
| 0.0009        | 19.0  | 4180 | 0.0842          | 0.9381    | 0.9536 | 0.9458 | 0.9868   |
| 0.0009        | 20.0  | 4400 | 0.0842          | 0.9376    | 0.9541 | 0.9458 | 0.9866   |


### Framework versions

- Transformers 4.44.2
- Pytorch 2.2.0+cu121
- Datasets 2.21.0
- Tokenizers 0.19.1
