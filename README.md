# CloudQuestions

Django Web-App for studying which creates an easier costumer experience for applying a mix between Flash Cards and Active Recall techniques.

:house: The home link is the following: https://cloudquestions.es/

## Summary

- [Contributing](#contributing)
- [Development](#development)
- [Tests](#tests)

## Contributing

Contributions are warmly welcomed. Doesn't have to be implementing new functionality, issues are also opened for documentation, support, etc. 

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Development

This instructions will get you up and running for development purposes. See testing for notes on how to test the app and special requests on tests created.

### Prerequisites

At CloudQuestions, we use environments for development (pyvenv). On these environments, we install the dependencies with pip.

### Installing steps
 
1. Fork this repository.
2. Clone your forked repository.
3. Set up your environment and dependencies.

```
python3 -m venv <environment_name>
pip install -r requirements.txt
```

At this point the app should be running locally. To run the Django server:

```
python manage.py runserver
```

Note: CloudQuestions uses API calls (auth, calendar events). Local development might malfunction if API keys are not provided to the environment. We use os to provide privacy on source files to important bits.

```python
import os
os.environ['NAME']
```

### API keys
As I said before, CloudQuestions uses API calls for some functionality. To be able to access the full experience when developing, we use a template to be included in the environment:

```
export DJANGO_SECRET='YOUR_DJANGO_KEY'
export EMAIL_HOST_USER='YOUR_EMAIL'
export EMAIL_HOST_PASSWORD='YOUR_EMAIL_PASSWORD'
export DEFAULT_FROM_EMAIL='YOUR_EMAIL'
export SERVER_EMAIL='YOUR_EMAIL'
export SOCIAL_AUTH_GITHUB_KEY='YOUR_KEY'
export SOCIAL_AUTH_GITHUB_SECRET='YOUR_KEY'
export SOCIAL_AUTH_TWITTER_KEY='YOUR_KEY'
export SOCIAL_AUTH_TWITTER_SECRET='YOUR_KEY'
export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='YOUR_KEY'
export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='YOUR_KEY'
export CALENDAR_CLIENT_ID='YOUR_KEY'
export CALENDAR_CLIENT_SECRET='YOUR_KEY'
export CALENDAR_API_KEY='YOUR_KEY'
export RECAPTCHA_PUBLIC_KEY='YOUR_KEY'
export RECAPTCHA_PRIVATE_KEY='YOUR_KEY'
```

To be able to include this template into your environment, fill the keys for the functionality you are interested in on the TEMPLATE_KEYS.txt file and include it the following way:

```
cat TEMPLATE_KEYS.txt >> <environment_name>/bin/activate
```

## Tests

We use pytest to run all our tests. It is included in the dependencies, so the only steps required are:

```
cd Cloudquestions_Web
pytest
```

We recommend writing tests on new functionality for an easier process for merging it to the repo.
