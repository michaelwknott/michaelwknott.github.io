Title: Schedule Jobs with GitHub Actions
Date: 2023-02-17 15:00
Category: Notes
Tags: github actions, notes
Slug:
Authors: Michael Knott
Summary: Using GitHub Actions to schedule ISSF World Rankings scraper.
Status: draft
#

### Change GitHub repo settings

This [stackoverflow post](https://stackoverflow.com/questions/73687176/permission-denied-to-github-actionsbot-the-requested-url-returned-error-403) solved the issue with the GitHub Action not running as scheduled:

To allow the scheduled job to run I needed to change the repo settings to allow both read and write permissions:

```
Settings
    -> Action
        -> General
            -> Workflow permissions and choose read and write permissions
            ```