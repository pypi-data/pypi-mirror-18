from setuptools import setup

setup(name='smple',
      version='0.2',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      install_requires=[
            'bs4'
      ],
      scripts=['bin/smple'],
      packages=['smple'],
      zip_safe=False)