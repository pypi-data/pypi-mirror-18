__date__ = "9/14/16"
__author__ = "Sharon Lev"
__email__ = "sharon_lev@yahoo.com"

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup


def filecontent_or_string(filename, string):
    content = string
    try:
        content = open(filename).read()
    except:
        pass
    return content

lic = filecontent_or_string('LICENSE', '')
readme = filecontent_or_string('README.md', 'Extra Unittest Functionality')

setup(
    name='unittestextras',
    version='1.0',
    packages= find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/sharonlev/pyUnittestExtras',
    license=lic,
    author='Sharon Lev',
    author_email='sharon_lev@yahoo.com',
    description='Extra Unittest Functionality',
    long_description=readme,
    test_suite='test'
)
