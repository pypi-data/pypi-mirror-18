from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pathinby',
      version='0.1',
      description=('Generate a hierarchy of the contents of a directory, '
                   'Possibly outputting to a file'),
      long_description=readme(),
      url='https://github.com/shockry/pathinby',
      author='Shokry',
      author_email='shokry92@gmail.com',
      license='MIT',
      include_package_data=True,
      test_suite='nose2.collector.collector',
      tests_require=['nose2'],
      entry_points={
        'console_scripts': ['pathinby=pathinby.pathinby:main'],
      },
      packages=['pathinby'])
