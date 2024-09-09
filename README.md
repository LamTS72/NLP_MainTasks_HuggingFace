# NLP Project

This repository contains several projects and implementations focused on Natural Language Processing (NLP) tasks. Each module demonstrates key concepts in NLP, using state-of-the-art models and techniques.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)


## Introduction

Natural Language Processing (NLP) is a rapidly evolving field in artificial intelligence, aiming to enable machines to understand, interpret, and respond to human language. This repository contains a variety of projects that explore different core tasks in NLP, ranging from language generation to translation and summarization.

## Features

The projects within this repository include:

1. **Named Entity Recognition (NER)**  
   Identifies and classifies proper names (e.g., people, organizations, locations) within a text, commonly used in model pre-training, such as BERT.

2. **Masked Language Model (MLM)**  
   Predicts masked tokens in a sentence, commonly used in model pre-training, such as BERT or DistilBERT.

3. **Causal Language Model (CLM)**  
   Generates text autoregressively by predicting the next token based on previous ones, used in models like GPT2.

4. **Summarization**  
   Automatically generates a concise summary of a longer document or text input, commonly used in model pre-training, such as T5 or mT5.

5. **Translation**  
   Translates text from one language to another using sequence-to-sequence models and used in MarianModel.

6. **Question Answering (QA)**  
   Provides direct answers to questions based on a given context or passage of text, commonly used in model pre-training, such as BERT.

## Technologies

This project utilizes the following technologies:
- Python
- Hugging Face Transformers
- PyTorch / TensorFlow
- NLTK / spaCy
- Seq2Seq and Transformer architectures
- Pretrained models such as BERT, GPT, T5, etc.

## Installation

To install and run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nlp-task.git
   cd nlp-task
2. Install the dependencies:
   ```bash
   pip install -r requirement.txt
3. Run the desired module (for example, NER):
   ```bash
   python3 nlp-task.py 
