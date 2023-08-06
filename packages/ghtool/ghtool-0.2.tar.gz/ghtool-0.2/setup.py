from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='ghtool',
    version='0.2',
    description='Simple CLI tool for github...',
    long_description=readme(),
    url='http://github.com/stojanovic-n/ghtool',
    author='Nikola Stojanovic',
    author_email='nikola.stojanovic91@outlook.com',
    license='MIT',
    entry_points = {
        'console_scripts': ['ghtool=ghtool.cli:main'],
    },
    packages=['ghtool'],
    install_requires=[
      'requests',
      'grequests'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    zip_safe=False)
