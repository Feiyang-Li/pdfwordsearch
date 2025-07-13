## 📚 Smart PDF Search

Smart PDF Search is a Python tool that enables intelligent search within PDF documents. Unlike traditional Ctrl+F, which only matches exact text, this tool ranks pages based on the appearance of keywords. It also leverages NLP techniques to find synonyms.

## Features

### Smart Search Bar

Use the smart search bar to query a pdf by keywords. The most relevant pages will be listed here.

![image](https://github.com/user-attachments/assets/56954926-bd96-4e59-8842-6ba5568af863)

### PDF Viewer
A pdf viewer is included in the project.
![image](https://github.com/user-attachments/assets/95d624d1-f6f8-4994-8cc0-b0156560dc8a)




### Reduced Memory Usage Compared to More Straightforward Techniques
A postings list data structure is created by the application to quickly perform queries. A straightforward implementation of a postings list can consume a lot of memory. We have managed to reduce the memory usage by 44% using variable length integer encoding.
![image](https://github.com/user-attachments/assets/c19f5751-d44b-4ff8-af54-be6821e268be)

Benchmarking code can be found in [benchmarking code](tests/benchmark_tests)

# Desktop Application

A Windows executable can be found [here](https://drive.google.com/file/d/1xATFucXB8-Kin1iGnrnCvNjnCp01Qd0H/view?usp=sharing)

