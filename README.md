# Markov AI SDK

Welcome to the Markov AI SDK 👋 
This SDK offers a robust framework for creating and deploying knowledge graphs with vector embeddings, 
enabling seamless data processing across various modalities for your projects.


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## Features

- **Modular Design**: Easily create and manage components of your pipeline.
- **Scalability**: Build knowledge graphs that can scale with your ever-increasing enterprise data.
- **User-Friendly**: Designed with simplicity in mind, making it accessible for both beginners and experienced developers.

## Installation

To install the MarkovAI Pipeline SDK, use pip:

```bash
pip install markov-ai
```
Make sure to have Python 3.8 or higher installed.

## Quick Start

Here's a quick example to get you started:

```
from markov-ai import Pipeline, Component

# Define your pipeline
pipeline = Pipeline()

# Add components to your pipeline
pipeline.add(Component('DataLoader', source='data/source.csv'))
pipeline.add(Component('ModelTrainer', model='RandomForest'))

# Run the pipeline
pipeline.run()
```

## Usage

The SDK allows you to define various components of your pipeline, such as data loaders, preprocessors, model trainers, and evaluators. 
You can customize each component to fit your specific needs.

### Example Components
* DataLoader: Load data from various sources (CSV, databases, etc.).
* Preprocessor: Clean and preprocess your data.
* ModelTrainer: Train your model using different algorithms.
* Evaluator: Evaluate the performance of your model.

## API Reference

For detailed information about the API and available components, please refer to the [API Documentation](https://markovai.xyz/docs).

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](https://markovai.xyz/contributing-guidelines) to get started.
