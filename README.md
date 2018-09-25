## Background

This is a simple Python script that emails users with a list of their Looks and highlights any Looks that haven't been accessed in the last 90 days.

**Note**: This is an experimental test to see what can be done using the Looker API and therefore is far from perfect. It is based on [this repository](https://github.com/llooker/python_api_samples).

## What you can find here
- A simple Looker API 3.0 SDK from [this repository](https://github.com/llooker/python_api_samples) in `lookerapi.py`
- A sample config.yml file for collecting API Tokens/Secrets
- A file for emailing users showing Looks that have not been used in the past 90 days in `email_users.py`

## Getting Started
- Update config.yml with your credentials for the Looker API and the Looker instance's hostname.
- Update the `<<email address>>` and `<<credentials for Google>>` after configuring you email and generating credentials to allow for sending emails from an unsecure application.
- Update the string of Looker users to email as `looker_user_ids = '1,2,3'`
- Run the file in the shell with `python email_users.py`.
