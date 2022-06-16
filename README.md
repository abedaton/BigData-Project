# About
This project is a university assignment for the Big Data course.
We were asked to choose an article and implement it.

We decided to go with [An efficient algorithm for distributed density-based outlier detection on big data](https://www.sciencedirect.com/science/article/abs/pii/S0925231215018500
).

## Installation
This project was coded using `python 3.8`.
You can use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries:

```bash
pip install -r requirements.txt
```

## Usage
The project allows multiple parameters:
```
-spython src/main.py -s "seed" -nt ""
```
|                      **Command**                       | **Shortcut** |                        **Description**                         | **additonal information** |
|:------------------------------------------------------:|:------------:|:--------------------------------------------------------------:|:-------------------------:|
|                       [-seed]()                        |      -s      |                         Sets the seed.                         |          `true`           |
|                   [-number_split]()                    |     -ns      |     Sets the number of splits per dimensions for the data.     |          `true`           |
|                         [-k]()                         |      /       | Sets K value used for multiple algorithms such as k-neighbors  |          `true`           |
|                   [-number_thread]()                   |     -nt      | Possible to write configurations created directly into a file. |          `true`           |
|                      [-no_plot]()                      |     -np      |                 Do not plot the result of LOF.                 |          `false`          |
|                       [-info]()                        |      -i      |                     Plots the info graph.                      |          `false`          |