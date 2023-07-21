AUTHOR = 'Michael Knott'
SITENAME = 'Michael Knott'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/michaelwknott'),
          ('github', 'https://github.com/michaelwknott'),
          ('linkedin','https://www.linkedin.com/in/michael-knott-a8005916/'))


DEFAULT_PAGINATION = 10

THEME = "/home/mwk/projects/blog/.venv/lib/python3.11/site-packages/pelican/themes/pelican-clean-blog"
SITESUBTITLE = u'Python Developer'


# Static files
STATIC_PATHS = [
    'images',
    'static/',
    ]

# pelican-clean-blog settings
HEADER_COVER = 'static/cool-background-black.png'
# HEADER_COLOR = 'black'
COLOR_SCHEME_CSS = 'tomorrow_night.css'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
