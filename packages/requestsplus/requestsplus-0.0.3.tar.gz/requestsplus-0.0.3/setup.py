from setuptools import setup, find_packages

setup(
    name = 'requestsplus',
    version = '0.0.3',
    keywords = ('requests==2.11.1', 'retries', 'web-scraping', 'auto-sleeping'),
    description = 'RequestsPlus is based on requests package, adding default retries, timeout, and auto-sleeping when requesting from a url',
    license = 'MIT License',
    install_requires = ['requests'],
    include_package_data=True,
    zip_safe=True,

    author = 'cchen',
    author_email = 'phantomkidding@gmail.com',

    url = 'https://github.com/PhantomKidding/RequestsPlus',

    packages = find_packages(),
    platforms = 'any',
)