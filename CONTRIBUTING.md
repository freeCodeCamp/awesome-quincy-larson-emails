# Contributing

Hello and welcome! Here are some notes on how to contribute to this repository.

**Contents**

- [Prerequisites](#prerequisites)
- [Files](#files)
- [Parsing files](#parsing-files)
- [Commits](#commits)

## Prerequisites

This repository aims to depend on as little dependencies as possible to make it simple.

Currently, all that is needed is Python and it's standard library.

## Files

```
.
├── convert_json.py    # Converts JSON to RSS
├── convert_readme.py  # Converts README into JSON
├── emails.json        # Weekly emails in JSON form
├── emails.rss         # Weekly emails in RSS form
├── LICENSE
└── README.md          # Weekly emails in Markdown form

0 directories, 6 files
```

The flow of information that these files are run in is `README.md > convert_readme.py > emails.json > convert_json.py > emails.rss`.

## Parsing files

There are two Python scripts that help parse and transform the Markdown information:

1. convert_json.py
2. convert_readme.py

## Commits

We try to adhere to Conventional Commits to make our commit messages more meaningful and semantic when possible. See here for some examples on how to make commit messages https://www.conventionalcommits.org/en/v1.0.0/.

Format: `<type>(<scope>): <subject>`

`<scope>` is optional

**Example:**

```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```

More Examples:

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)

Source: https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716
