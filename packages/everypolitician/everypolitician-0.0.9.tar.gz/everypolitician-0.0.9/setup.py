from setuptools import setup, find_packages
setup(
    name = "everypolitician",
    version = "0.0.9",
    packages = find_packages(),
    author = "Mark Longair",
    author_email = "mark@mysociety.org",
    description = "Navigate countries and legislatures from EveryPolitician",
    license = "AGPL",
    keywords = "politics data civic-tech",
    install_requires = [
        'requests',
        'six >= 1.9.0',
        'everypolitician-popolo >= 0.0.8',
    ]
)
