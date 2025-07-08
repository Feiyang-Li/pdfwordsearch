## 📚 Smart PDF Search

Smart PDF Search is a Python tool that enables intelligent search within PDF documents. Unlike traditional Ctrl+F, which only matches exact text, this tool ranks pages based on the appearance of keywords. It also leverages NLP techniques to find synonyms.

## Features

### Reduced Memory Usage Compared to More Straightforward Techniques
We have managed to reduce the memory usage by 44% using variable length integer encoding.
![image](https://github.com/user-attachments/assets/c19f5751-d44b-4ff8-af54-be6821e268be)

Benchmarking code can be found in [benchmarking code](tests/benchmark_tests)

# Applications

## Desktop Application

### Installation

### Usage

## CLI

### Requirements
- Poetry

#### Installation
Use ``poetry install`` to install all the packages required by pdfwordsearch

### Usage
Within the ``src/pdfwordsearch`` directory run the following
```
python main.py [pdf file path]
```


