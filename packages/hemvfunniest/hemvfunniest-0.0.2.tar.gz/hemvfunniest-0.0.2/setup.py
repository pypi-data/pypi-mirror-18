from setuptools import setup

setup(name='hemvfunniest',
      version='0.0.2',
      description='The funniest joke in the world',
      url='https://bitbucket.org/hemv/hemv_funniest.git',
      author='hemv',
      author_email='vichet.hem@gmail.com',
      license='MIT',
      packages=['hemvfunniest'],
      install_requires = [
            'markdown'
      ],
      zip_safe=False)