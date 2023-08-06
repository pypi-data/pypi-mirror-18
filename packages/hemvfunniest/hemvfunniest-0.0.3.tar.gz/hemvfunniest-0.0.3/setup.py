from setuptools import setup

def readme():
      with open('README.rst') as f:
            return f.read()

setup(name='hemvfunniest',
      version='0.0.3',
      description='The funniest joke in the world',
      url='https://bitbucket.org/hemv/hemv_funniest.git',
      author='hemv',
      author_email='vichet.hem@gmail.com',
      license='MIT',
      packages=['hemvfunniest'],
      install_requires = [
            'markdown'
      ],
      include_package_data=True,
      zip_safe=False)