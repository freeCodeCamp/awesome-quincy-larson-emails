# Contributing

Hello and welcome! Here are some notes on how to contribute to this repository.

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

## Parsing files

There are two Python scripts that help parse and transform the Markdown information:

1. convert_json.py
2. convert_readme.py
