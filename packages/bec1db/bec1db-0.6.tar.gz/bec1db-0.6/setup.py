from setuptools import setup

setup(name='bec1db',
      version='0.6',
      description='The hackiest database reader ever',
      author='biswaroop',
      author_email='mail.biswaroop@gmail.com',
      license='MIT',
      packages=['bec1db'],
      install_requires=[
          'pandas'
      ],
      url='https://github.com/biswaroopmukherjee/bec1db',
      download_url = 'https://github.com/biswaroopmukherjee/bec1db/tarball/0.4',
      zip_safe=False)
