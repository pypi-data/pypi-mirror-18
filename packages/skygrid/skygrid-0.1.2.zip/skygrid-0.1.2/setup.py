from distutils.core import setup
setup(
  name = 'skygrid',
  packages = ['skygrid'],
  version = '0.1.2',
  description = 'The SkyGrid Python SDK',
  author = 'SkyGrid',
  author_email = 'hey@skygrid.io',
  license='MIT',
  install_requires=[
    'socketIO_client',
  ],
  url = 'https://github.com/skygridio/skygrid-sdk-python',
  keywords = ["skygrid", "iot", "internet of things"],
  classifiers = [],
)