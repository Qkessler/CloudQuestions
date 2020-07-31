# Introduction

Contributions are warmly welcome! Feel free to tackle an issue on the issues tab!

:bulb: Issues are opened for all types of contributions: bugs, styling, documentation, typos, testing, etc! If you wanna be part of the community and don't know how to code there is plenty you can do!

# Pull requests format

Pull requests must have a title reflecting the functionality implemented. Also, comments on the functionality implemented including the issue number and comments for an easier reviewing process.

# Pull request process

At CloudQuestions we use Git flow. We have a "master" branch that reflects the production code. Starting at "master", we also have a "dev" branch, where all the features are created for the next release! 

Contributors create branches starting at "dev" and when they are done the open a pull request to "dev". Pull requests are reviewed. If everything is working, they are merged into the dev branch.

The way we operate can be summarized with the following steps:

1. Clone the repo.
2. Checkout to the dev branch.
3. Create a new branch off the dev branch.
4. Checkout to that new branch and start contributing!
5. When done, create tests (pytest) and if everything is ok, open a pull request to the dev branch.
6. Contribution is merged!

# Testing

Tests are created to make sure no existing functionality is broken after certain changes.

At CloudQuestions we use pytest. Pull requests must pass all tests created and add new tests testing new functionality added.

Take a look at pytest documentation, they have a pretty straight forward Getting Started section!