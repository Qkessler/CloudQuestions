# CloudQuestions

Django Web-App for studying which creates an easier costumer experience for applying a mix between Flash Cards and Active Recall techniques.

:house: The home link is the following: https://cloudquestions.es/
    
:warning: CloudQuestions is not yet in production, localhost server development at the moment.

    

## Summary

- [Contributing](#contributing)
- [Development](#development)
- [Tests](#tests)
- [Licence](#licence)

## Contributing

Contributions are warmly welcomed. Doesn't have to be implementing new functionality, issues are also opened for documentation, support, etc. 

Please read [CONTRIBUTING.md](https://github.com/Qkessler/CloudQuestions/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Development

This instructions will get you up and running for development purposes. See testing for notes on how to test the app and special requests on tests created.

### Prerequisites

At CloudQuestions, we use environments for development pyvenv. On these environments, we install the dependencies with pip.

### Installing steps
 
2. Clone this repository.
3. Checkout to the "dev" branch:
    ```
    git checkout dev
    ```
4. Create a new branch off the "dev" branch:
    ```
    git checkout -b <new_branch_name>
    ```
5. Add [EXCLUDE](https://github.com/Qkessler/CloudQuestions/blob/master/EXCLUDE.txt) info to avoid unwanted files.
    
    ```
    cat EXCLUDE.txt >> .git/info/exclude
    ```
    
6. Set up your environment and dependencies:

```
python3 -m venv <environment_name>
pip install -r requirements.txt
```
    
At this point the app should be running locally. To create migrations and create the database.

```    
python manage.py makemigration questions accounts
python manage.py migrate    
```    
    
To run the Django server:

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

To be able to include this template into your environment, fill the keys for the functionality you are interested in on the [TEMPLATE_KEYS.txt](https://github.com/Qkessler/CloudQuestions/blob/master/TEMPLATE_KEYS.txt) file and include it the following way:

```
cat TEMPLATE_KEYS.txt >> <environment_name>/bin/activate
```

## Tests

We use [pytest](https://docs.pytest.org/en/stable/contents.html) to run all our tests. It is included in the dependencies, so the only steps required are:

```
cd CloudQuestions_Web
pytest
```

We recommend writing tests on new functionality for an easier process for merging it to the repo.

### Format tests.

We use [Black](https://black.readthedocs.io/en/stable/) formatter at CloudQuestions. To test files to have a black format:

```
pytest --black    
```           

## Licence
This project is licenced under the [MIT](https://github.com/Qkessler/CloudQuestions/blob/master/LICENSE) Licence - see the [LICENCE](https://github.com/Qkessler/CloudQuestions/blob/master/LICENSE) for details.        
