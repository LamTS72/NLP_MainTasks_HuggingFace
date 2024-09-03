---
library_name: transformers
license: apache-2.0
base_model: bert-base-cased
tags:
- generated_from_keras_callback
model-index:
- name: Chessmen/TF_fine_tune_bert-base-cased
  results: []
---

<!-- This model card has been generated automatically according to the information Keras had access to. You should
probably proofread and complete it, then remove this comment. -->

# Chessmen/TF_fine_tune_bert-base-cased

This model is a fine-tuned version of [bert-base-cased](https://huggingface.co/bert-base-cased) on an unknown dataset.
It achieves the following results on the evaluation set:
- Train Loss: 0.0550
- Validation Loss: 0.0649
- Epoch: 6

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- optimizer: {'name': 'AdamWeightDecay', 'learning_rate': {'module': 'keras.optimizers.schedules', 'class_name': 'PolynomialDecay', 'config': {'initial_learning_rate': 2e-05, 'decay_steps': 1756, 'end_learning_rate': 0.0, 'power': 1.0, 'cycle': False, 'name': None}, 'registered_name': None}, 'decay': 0.0, 'beta_1': 0.9, 'beta_2': 0.999, 'epsilon': 1e-08, 'amsgrad': False, 'weight_decay_rate': 0.01}
- training_precision: mixed_float16

### Training results

| Train Loss | Validation Loss | Epoch |
|:----------:|:---------------:|:-----:|
| 0.1439     | 0.0649          | 0     |
| 0.0545     | 0.0649          | 1     |
| 0.0546     | 0.0649          | 2     |
| 0.0552     | 0.0649          | 3     |
| 0.0550     | 0.0649          | 4     |
| 0.0540     | 0.0649          | 5     |
| 0.0550     | 0.0649          | 6     |


### Framework versions

- Transformers 4.44.2
- TensorFlow 2.17.0
- Datasets 2.21.0
- Tokenizers 0.19.1
