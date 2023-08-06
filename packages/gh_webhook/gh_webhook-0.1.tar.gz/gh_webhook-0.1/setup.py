from setuptools import setup

setup(name='gh_webhook',
      version='0.1',
      description='Webhook for github',
      url='https://github.com/GerbenAaltink/py-gdw',
      author='Gerben Aaltink',
      author_email='gerbenaaltink@gmail.com',
      license='MIT',
      packages=['gh_webhook'],
      zip_safe=False,
      install_requires=[
          'bottle==0.12.10',
          'click==6.6',
      ],
)