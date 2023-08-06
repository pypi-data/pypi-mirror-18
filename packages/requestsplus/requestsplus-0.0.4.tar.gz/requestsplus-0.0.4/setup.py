from setuptools import setup, find_packages

setup(
    name = 'requestsplus',
    version = '0.0.4',
    keywords = ('requests', 'retries', 'web-scraping', 'auto-sleeping'),
    description = 'RequestsPlus is based on requests package, adding default retries, timeout, and auto-sleeping when requesting from a url',
    license = 'MIT License',
    install_requires = ['requests==2.11.1'],
    include_package_data=True,
    zip_safe=True,

    author = 'cchen',
    author_email = 'phantomkidding@gmail.com',

    url = 'https://github.com/PhantomKidding/RequestsPlus',

    packages = find_packages(),
    platforms = 'any',
)