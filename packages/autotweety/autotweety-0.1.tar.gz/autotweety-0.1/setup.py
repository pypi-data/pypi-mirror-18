from setuptools import setup,find_packages
setup(
  name = 'autotweety',
  packages = find_packages(exclude=["env"]),
  version = '0.1',
  description = 'Something that tweets',
  author = 'localhuman',
  author_email='tasaunders@gmail.com',
  url = 'https://github.com/localhuman/autotweet', # use the URL to the github repo
  download_url = 'https://github.com/localhuman/autotweet/tarball/master', # I'll explain this in a second
  keywords = ['twitter','@realDonaldTrump'], # arbitrary keywords
  classifiers = [],
  install_requires = ['python-twitter'],
)