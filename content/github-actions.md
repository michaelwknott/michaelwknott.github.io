Title: ISSF World Rankings Scraper using GitHub Actions
Date: 2023-03-26 22:00
Category: Notes
Tags: github actions, projects, notes
Authors: Michael Knott
Summary: Using GitHub Actions to schedule ISSF World Rankings scraper.
Status:

### ISSF World Rankings

The ISSF website provides a page that lists the current World Rankings for each event. For example, this [link](https://www.issf-sports.org/competitions/worldranking/complete_ranking_by_event_yearly.ashx?evlinkid=ARM) shows the World Rankings for Men's 10m Air Rifle. The ISSF only provides the latest World Rankings. With each update the previous World Ranking data is no longer available.
I wanted to scrape the World Rankings on a weekly basis to track the performance of athletes I support. Having historical data would also be useful for future analysis.

I created a Python script to scrape, parse and store data for each of the 12 Olympic Shooting events. I then needed a way to run the script on a weekly basis. At first I used a Deepnote environment due to the simplicity of setting up scripts to run on a schedule. But, I wanted to find a way to utilise my existing local development setup of VS Code, Git and GitHub. After reading a [blog post](https://simonwillison.net/2020/Oct/9/git-scraping/) by Simon Willison, I realised I'd be able to use GitHub Actions to achieve this.

### GitHub Actions
GitHub Actions allows the creation of workflows triggered by events. Each workflow consists of one or more jobs, each containing steps that perform an action or run a shell command. In my case I wanted to create a workflow that runs a Python script on a weekly basis.

You configure workflows in a YAML file and save it at the root of your project/GitHub repo in a `.github/workflows` directory. I named my workflow file `schedule.yaml`. This created the following filepath for my workflow:

```
issf_world_rankings
├── .github
    └── workflows
        └── schedule.yaml
```


The first element of the `schedule.yaml` file should define the name of the workflow. I called my workflow `Schedule ISSF Scraper`and mapped it to the `name` key using the following syntax:

```
# schedule.yaml

name: Schedule ISSF Scraper
```

The next step is to define the event that will trigger the workflow. GitHub Actions provides multiple [events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) that can be used as triggers. For this project I utilised `workflow_dispatch` and `schedule`. The `workflow_dispatch` event allows you to manually start the workflow from the actions tab of your GitHub repo (see `run workflow` button in the image below).

![Workflow Dispatch]({static}/images/github-actions-workflow-dispatch.png)

 The `schedule` event triggers a workflow to run at a scheduled time using [cron syntax](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07). I scheduled my workflow to run at 09:27 every Friday. I mapped both events to the `on` key in the `schedule.yaml` file:

```
# schedule.yaml

on:
  workflow_dispatch:
  schedule:
  - cron: "27 09 * * 5"
```

Defining the job or jobs associated with the workflow comes next. For this project I have a single job with the id `scrape_data` to which I map the jobs configuration data. Each job runs on it's own runner (a hosted virtual environment). You define the type of operating system for the runner using the `runs-on` key. In this case I've defined the job to run on the latest version of Ubuntu:

```
# schedule.yaml

jobs:
  scrape_data:
    runs-on: ubuntu-latest 
```

Each job consists of several steps that run in sequential order and perform an action or shell command. An action is a reusable program that performs a specific task.  In the YAML workflow file you map actions to the `uses` key. Actions are available at [GitHub Marketplace](https://github.com/marketplace?category=&query=&type=actions&verification=) or custom actions can be created using the following [documentation](https://docs.github.com/en/actions/creating-actions). A shell command is a instruction to the runner's operating system. In the YAML workflow file you map shell commands to the `run` key.

My `scrape_data` job has six steps nested within the `steps` key:

```
steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: Set up Python 3.11
        uses: actions/setup-python@v2
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Scrape data
        run: python3 scraper.py
      - name: Git commit
        run: |
          git add .
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          timestamp=$(date -u +%F)
          git commit -m "Latest data: ${timestamp}"
      - name: Git push
        run:
          git push
```

+ Step 1 in my `scrape_data`job uses `actions/checkout@v3` to check out the repository's code onto the runner. The `with` key passes extra inputs to the associated action. I use the `with` key to pass the input `fetch-depth: 0`. This instructs `actions/checkout@v3` to fetch the history for all branches of the repo.

+ Step 2 uses `actions/setup-python@v2` to install Python on the runner. The `with` key passes the input `python-version: "3.11"`and states that I want Python 3.11 installed on the runner.

+ Step 3 runs the pip command to install the required dependencies for the `scraper.py` script.

+ Step 4 uses the pythons command to run `scraper.py`.

+ Step 5 uses git to add the file changes in the repo to version control. The `|` symbol indicates that the mapped values to the `run` key should be interpreted as individual values and run as individual commands. 

+ Step 6 uses git to push the changes to GitHub.

#### My Workflow File

For clarity the full workflow YAML file is included below:
```
# schedule.yaml

name: Schedule ISSF Scraper
on:
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:
  schedule:
  - cron: "27 09 * * 5"
jobs:
  scrape_data:
    runs-on: ubuntu-latest 
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: Set up Python 3.11
        uses: actions/setup-python@v2
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Scrape data
        run: python3 scraper.py
      - name: Git commit
        run: |
          git add .
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          timestamp=$(date -u +%F)
          git commit -m "Latest data: ${timestamp}"
      - name: Git push
        run:
          git push
```



#### Additional Notes

To allow the scheduled job to run I needed to change the repo settings to allow both read and write permissions. This [stackoverflow post](https://stackoverflow.com/questions/73687176/permission-denied-to-github-actionsbot-the-requested-url-returned-error-403) solved the issue with the GitHub Action not running as scheduled.

#### Useful resources
YAML documentation including syntax is available [here](https://yaml.org/).