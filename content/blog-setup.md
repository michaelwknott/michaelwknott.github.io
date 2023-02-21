Title: Pelican Blog Setup
Date: 2023-02-08 12:00
Modified: 2023-02-08 14:05
Category: Notes
Tags: pelican, notes
Slug:
Authors: Michael Knott
Summary: The steps I took to set-up this blog.

# How I Set-up this Pelican Blog

This post will act as a personal reminder on how I set-up this blog.

### Create a GitHub repo
I created an empty GitHub repo without a README.md file and used the following format when naming the repo - `username.github.io`. Username is changed to your GitHub username. My repo has the following name `michaelwknott.github.io`.

### Create project directory and Python virtual environment

Within my projects directory, I created a new directory called blog:

`mkdir blog`

`cd blog`

I initialised the directory as a git repositiory, created a Python virtual environment and added the the virtual environment to a .gitignore file:

`git init`

`python -m venv .venv --prompt .`

`echo .venv >> .gitignore`

I add the .gitignore file to be tracked by git:

`git add .`

and created an initial commit:

`git commit -m "Initial commit"`

I linked the blog directory with the GitHub repo, renamed the master branch to main and pushed the main branch to GitHub:

`git remote add origin git@github.com:michaelwknott/michaelwknott.github.io.git`

`git branch -M main`

`git push origin main`


### Add project dependencies

I use pip-tools to manage project dependencies as it provides greater detail on why each dependency is installed. I can easily assess whether a package is directly required by my project or a transitive package that is installed as a dependency.

I activated my virtual environment and installed pip-tools using the following commands:

`source .venv/bin/activate`

`python -m pip install pip-tools`

With pip-tools I add the directly required packages to a requirements.in file:

`echo "pelican[markdown]">=4.8.0 >> requirements.in`		

`echo ghp-import>=2.1.0 >> requirements.in`

At the time of writing 4.8.0 was the latest version of Pelican. As I am using markdown to write my blog articles I've followed the dcoumentation guidance and installed markdown with Pelican. ghp-import is used to copy the output directory onto the main branch, which GitHub Pages uses to serve the blog site.

Next I ran the following command:

`pip-compile requirements.in`

This created a requirements.txt file with a list of all installed packages and whether they are installed as a direct or transitive dependency.
With the requirement.txt file created, I ran the following command to install the packages:

`python -m pip install -r requirements.txt`

### A note on how GitHub Pages works

A note on how GitHub Pages works: My blog will be published when changes are pushed to the main branch. See [documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

To publish the blog, Github pages will search for an entry file (index.html file for a Pelican site) in the root of the blog directory (output directory for a Pelican site) on the main branch.

Due to the above, I created a content branch to store all the Pelican configuration files and raw markdown files. From the content branch I push the output directory to the main branch, which GitHub Pages will use to publish the blog. This separates the configuration and markdown files used to make the blog and the theme files and generated html files required for GitHub Pages to serve the blog as a website.

### Creating the Pelican blog

I created and checked out a new branch using the following command:

`git checkout -b content`

and ran the following command to generate the Pelican site:

`pelican-quickstart`

I provided the following answers to the Pelican site generator:

```
Welcome to pelican-quickstart v4.8.0.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.


> Where do you want to create your new web site? [.]
> What will be the title of this web site? A Tech Journey
> Who will be the author of this web site? Michael Knott
> What will be the default language of this web site? [en]
> Do you want to specify a URL prefix? e.g., https://example.com   (Y/n) n
> Do you want to enable article pagination? (Y/n) Y
> How many articles per page do you want? [10]
> What is your time zone? [Europe/Rome] GMT
> Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n) Y
> Do you want to upload your website using FTP? (y/N) N
> Do you want to upload your website using SSH? (y/N) N
> Do you want to upload your website using Dropbox? (y/N) N
> Do you want to upload your website using S3? (y/N) N
> Do you want to upload your website using Rackspace Cloud Files? (y/N) N
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
```

### Add content

To add content, I navigated to the content directory and created a new markdown file:

`touch pybites-podcast.md`

and added the following:

```
Title: Pybites Podcast
Date: 2023-02-08 12:05
Category: Python, Pybites, Podcast
Summary: My first Podcast Appearance. I share my journey with Python and my experience of the Pybites PDM programme.


# My First Podcast Appearance


Thanks to Bob and Julian for having me on the Pybites podcast. I share my journey with Python and my experience of the Pybites PDM programme.

Click [here](https://pybit.es/articles/how-michael-knott-used-python-to-enhance-his-sports-coaching-career/) to have a listen.

Check out [Pybites](https://pybit.es/) and their [PDM](https://pybit.es/catalogue/the-pdm-program/) programme.
```

I also and created a directory called pages and added an about.md file:

`cd content`

`mkdir pages`

`touch about.md`

I added the following to about.md:

```
title: About
date: 2023-02-08 12:00

Hi, I'm Michael.

I'm a Strength and Conditioning Coach and Python Developer.

I'm currently using Python to solve performance problems for the coaches and athletes I support.

This blog will be a place for me to store and collate the things I learn as I continue to utilise Python on a daily basis.
```
### Commit the changes

I ran the following commands to create my second commit and push the changes to GitHub:

`git add .`

`git commit -m 'initial pelican commit to content'`

`git push origin content`

### Check the site is properly configured by running a development server

To view the website locally I ran:

`pelican content -o output -s publishconf.py`

`pelican --autoreload --listen`

I navigated to localhost8000 in my browser to view the the blog site.

### Publish the blog

I navigated to the blog directory and ran the following command to generate the html files required to serve the blog:

`pelican content -o output -s publishconf.py`

and ran the following command to copy the output directory onto the main branch:

`ghp-import -m "Generate Pelican site" --no-jekyll -b main output`

Finally, I pushed the main branch (containing the index.html file in the output directory that GitHub uses as the entry point to serve the blog site):

`git push origin main`

The blog is available at <https://michaelwknott.github.io>


### Adding a Pelican theme

I used the pelican-clean-blog theme for my blog site. To add the theme to Pelican I utilsed the following steps. I copied the name of the github repo:

`git@github.com:gilsondev/pelican-clean-blog.git`

In my projects directory (the parent directory of blog) I created a folder called pelican-themes. I navigated into the newly created pelican-themes directory and cloned the repo:

`git clone git@github.com:gilsondev/pelican-clean-blog.git`

With the repo cloned, I navigated back to my blog directory and installed the pelican theme:

`pelican-themes --install /home/mwk/projects/pelican-themes/pelican-clean-blog --verbose`

pelican-themes is the command line tool for managing themes. The documentation is available [here](https://docs.getpelican.com/en/stable/pelican-themes.html). You use the --install (-i) command to install themes. It takes the path (/home/mwk/projects/pelican-themes/pelican-clean-blog) to the theme as an arguement.

I ran the following command to get the path to the pelican-clean-blog theme:

`pelican-themes --list --verbose`

This returned a list of paths to all the currently installed themes:

`/home/mwk/projects/blog/.venv/lib/python3.11/site-packages/pelican/themes/pelican-clean-blog`

I add the path to the THEME variable in pelicanconf.py file:

`THEME = "/home/mwk/projects/blog/.venv/lib/python3.11/site-packages/pelican/themes/pelican-clean-blog"`

To finish I added all changes to version control, commited the changes and pushed the content branch to GitHub. Finally, I rebuilt the site and pushed the main branch to GitHub using the following commands:

`pelican content -o output -s publishconf.py`

`ghp-import -m "Generate Pelican site" --no-jekyll -b main output`

`git push origin main`


### Useful links

I found the following links useful to set-up the blog:

+ A useful [blog](https://opensource.com/article/19/5/run-your-blog-github-pages-python) by Erik O'Shaughnessy on how to set-up Pelican with GitHub Pages.
+ How to set-up [custom themes](https://geekyshacklebolt.wordpress.com/2020/08/18/how-to-use-a-custom-pelican-blog-theme/) for Pelican by Shiva Saxena.




