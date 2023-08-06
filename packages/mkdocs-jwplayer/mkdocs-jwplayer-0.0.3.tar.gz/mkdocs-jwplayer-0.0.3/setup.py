from setuptools import setup, find_packages

setup(
  name='mkdocs-jwplayer',
  version='0.0.3',
  url='https://github.com/jwplayer/mkdocs-jwplayer',
  license='',
  description='JW Player theme for MkDocs',
  author='Matthew Martindale',
  author_email='mmartindale@jwplayer.com',
  packages=find_packages(),
  include_package_data=True,
  entry_points={
    'mkdocs.themes': [
      'jwplayer = jwplayer',
    ]
  },
  zip_safe=False
)
