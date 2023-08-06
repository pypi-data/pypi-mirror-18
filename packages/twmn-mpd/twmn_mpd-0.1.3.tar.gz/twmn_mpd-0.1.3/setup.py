from setuptools import setup

setup(name='twmn_mpd',
      version='0.1.3',
      description='A simple mpd notifier for twmn',
      url='http://github.com/mrkgnao/twmn-mpd',
      author='Soham Chowdhury',
      author_email='chow.soham@gmail.com',
      license='MIT',
      packages=['twmn_mpd'],
      install_requires=[
          'python-mpd2'
      ],
      scripts=[
          'mpd_twmn_notifier'
      ],
      zip_safe=False)
