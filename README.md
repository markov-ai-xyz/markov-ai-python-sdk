[![Downloads](https://static.pepy.tech/badge/markov-ai)](https://pepy.tech/project/markov-ai)

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

To install the Markov AI SDK, use pip:

```bash
pip install markov-ai
```
Make sure to have Python 3.8 or higher installed.

## Quick Start

Here's a quick example to get you started:

```
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('MARKOV_AI_API_KEY')
db_uri = os.getenv('DB_URI')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

from markov_ai import Component, DatabaseService, Destination, Pipeline

destination = Destination.from_credentials(DatabaseService.NEO4J, db_uri, db_user, db_password)
pipeline = Pipeline(api_key=api_key, destination=destination)

component = Component('DataLoader', source='./sample_content/apple.txt')
pipeline.add(component)

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
