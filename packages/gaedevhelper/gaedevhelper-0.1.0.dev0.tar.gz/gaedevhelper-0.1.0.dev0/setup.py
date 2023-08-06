from setuptools import setup

setup(name='gaedevhelper',
      version='0.1.0.dev',
      description='A lovely command-line helper for developing GAE applications',
      url='https://github.com/devjoe/gae-dev-helper',
      author='devjoe',
      author_email='excusemejoe@gmail.com',
      license='MIT',
      packages=['gaedevhelper'],
      install_requires=[
          'Click',
          'Pygments',
          'subprocess32',
          'daemonize',
      ],
      tests_require=[
          'pytest',
          'pytest-mock'
      ],
      entry_points='''
            [console_scripts]
            gaedh=gaedevhelper.gae:gae
      ''',
      keywords=['GAE', 'Google App Engine', 'dev_appserver', 'pygments', 'remote_api', 'gae_dev_helper'],
      zip_safe=False,
      classifiers=[ 'Programming Language :: Python',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.1',
                    'Programming Language :: Python :: 3.2',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Topic :: Software Development',
                    'Topic :: System :: Networking',
                    'Topic :: Terminals',
                    'Topic :: Text Processing',
                    'Topic :: Utilities' ],
      )
