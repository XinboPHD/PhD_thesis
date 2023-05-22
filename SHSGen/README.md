# Topic-Generation
---------------------------------------

# Introduction
This tool is the protype code of the tool in 
Paper "Topic Generation",
a Machine Learning based topic generation for smart home securtiy and safety.

# Framework
Here are Four components:
1. Real Scenario Collection
2. Fine-tuning for Specific Task
3. Scenario Generation
4. Topic Generation

![Workflow](https://github.com/BeauBan/Topic-Generation/blob/main/images/workflow.png)

# Usage
This repository is meant to be a starting point for researchers and engineers to experiment for smart home topic generation.

## Real Scenario Collection
This component is accomplished through either web crawler or suevey methodology. 
Here is the publicly avaliable dataset that can be downloaded.

## Fine-tuning for Specific Task
This component has been built and runing using Java on Goole Colab. 
We use gpt-2-simple package that 
that wraps existing model fine-tuning and generation scripts for OpenAI's GPT-2 text generation model 
We use GPU for fine-tuning and here is the script.
In paper, we use 355M model for experiments as the model size has better performance. 
It is a open research question in future.

## Scenario Generation
Scenario generation is also built on Google Colab using the gpt-2-simple package. 
The GPU is used for generation based on the fine-tuned model.

## Topic Generation
This component outputs the topics though topic modeling. 
Given generated scearios,
though semantic embedding and topic modeling technique,
we create topics for the scearnios.
We use BERTopic, 
that leverages transformers and c-TF-IDF to create dense clusters allowing for easily interpretable topics whilst keeping important words in the topic descriptions.
It supports visualizations similar to LDAvis!


<!-- # Citation
 -->












