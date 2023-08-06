from setuptools import setup

setup(name='twmn_mpd',
      version='0.1.5',
      description='A simple mpd notifier for twmn',
      url='http://github.com/mrkgnao/twmn-mpd',
      author='Soham Chowdhury',
      author_email='chow.soham@gmail.com',
      license='MIT',
      packages=['twmn_mpd', 'twmn_mpd.providers'],
      install_requires=[
          'python-mpd2'
      ],
      entry_points={
          'console_scripts': [
              'mpd_twmn_notifier = twmn_mpd.TWMNSocketClient:start_notifs'
          ]
      },
      zip_safe=False)
