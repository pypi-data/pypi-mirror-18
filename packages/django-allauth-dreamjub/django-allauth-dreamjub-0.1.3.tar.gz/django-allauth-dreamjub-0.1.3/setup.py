from distutils.core import setup
setup(
  name = 'django-allauth-dreamjub',
  packages = ['dreamjub', 'dreamjub.providers', 'dreamjub.providers.oauth'], # this must be the same as the name above
  version = '0.1.3',
  description = 'An OAuth provider for django-allauth and dreamjub',
  author = 'Leonhard Kuboschek',
  author_email = 'pypi@hw.is',
  url = 'https://github.com/kuboschek/allauth-testbed', # use the URL to the github repo
  download_url = 'https://github.com/kuboschek/allauth-testbed/tarball/0.1.3', # I'll explain this in a second
  keywords = ['django', 'allauth', 'login'], # arbitrary keywords
  classifiers = [],
)
