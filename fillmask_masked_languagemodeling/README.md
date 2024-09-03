---
library_name: transformers
license: apache-2.0
base_model: distilbert-base-uncased
tags:
- generated_from_trainer
model-index:
- name: fine_tune_distilbert-base-uncased
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# fine_tune_distilbert-base-uncased

This model is a fine-tuned version of [distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased) on an unknown dataset.
It achieves the following results on the evaluation set:
- Loss: 2.1226
- Model Preparation Time: 0.0016

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
- mixed_precision_training: Native AMP

### Training results

| Training Loss | Epoch | Step  | Validation Loss | Model Preparation Time |
|:-------------:|:-----:|:-----:|:---------------:|:----------------------:|
| 2.5551        | 1.0   | 767   | 2.3648          | 0.0016                 |
| 2.4329        | 2.0   | 1534  | 2.3181          | 0.0016                 |
| 2.3874        | 3.0   | 2301  | 2.2831          | 0.0016                 |
| 2.3409        | 4.0   | 3068  | 2.2422          | 0.0016                 |
| 2.3124        | 5.0   | 3835  | 2.2302          | 0.0016                 |
| 2.2895        | 6.0   | 4602  | 2.2104          | 0.0016                 |
| 2.2649        | 7.0   | 5369  | 2.2014          | 0.0016                 |
| 2.2445        | 8.0   | 6136  | 2.1939          | 0.0016                 |
| 2.234         | 9.0   | 6903  | 2.1776          | 0.0016                 |
| 2.2142        | 10.0  | 7670  | 2.1607          | 0.0016                 |
| 2.208         | 11.0  | 8437  | 2.1682          | 0.0016                 |
| 2.1933        | 12.0  | 9204  | 2.1530          | 0.0016                 |
| 2.1808        | 13.0  | 9971  | 2.1493          | 0.0016                 |
| 2.1689        | 14.0  | 10738 | 2.1422          | 0.0016                 |
| 2.1598        | 15.0  | 11505 | 2.1347          | 0.0016                 |
| 2.1567        | 16.0  | 12272 | 2.1373          | 0.0016                 |
| 2.1458        | 17.0  | 13039 | 2.1270          | 0.0016                 |
| 2.1475        | 18.0  | 13806 | 2.1200          | 0.0016                 |
| 2.141         | 19.0  | 14573 | 2.1312          | 0.0016                 |
| 2.1423        | 20.0  | 15340 | 2.1202          | 0.0016                 |


### Framework versions

- Transformers 4.44.2
- Pytorch 2.2.0+cu121
- Datasets 2.21.0
- Tokenizers 0.19.1
