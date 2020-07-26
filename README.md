# CloudQuestions

Django Web-App for studying which creates an easier costumer experience for applying a mix between Flash Cards and Active Recall techniques.

## Summary

    - [Getting started](#getting-started)

## Getting Started

This instructions will get you up and running for development purposes. See testing for notes on how to test the app and special requests on tests created.

### Prerequisites

At CloudQuestions, we use environments for development (pyvenv). On these environments, we install the dependencies with pip.

### Installing steps

```
git clone https://github.com/Qkessler/CloudQuestions.git
python3 -m venv .env
pip install -r requirements.txt
```

At this point the app should be running locally.
Note: CloudQuestions uses API calls (auth, calendar events). Local development might malfunction if API keys are not provided to the environment. We use os to provide privacy on source files to important bits.

```python
import os
os.environ['NAME']
```

