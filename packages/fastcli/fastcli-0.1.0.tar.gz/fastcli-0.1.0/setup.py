import re
from setuptools import setup, find_packages

try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst')
    history = pypandoc.convert('HISTORY.md', 'rst')
except (ImportError, OSError):
    with open('README.md') as readme_file, open('HISTORY.md') as history_file:
        readme = readme_file.read()
        history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

with open('requirements-dev.txt') as dev_requirements_file:
    dev_requirements = dev_requirements_file.read().splitlines()

version_regex = re.compile(r'__version__ = [\'\"]((\d+\.?)+)[\'\"]')
with open('src/fastcli/__init__.py') as f:
    vlines = f.readlines()
__version__ = next(re.match(version_regex, line).group(1) for line in vlines
                   if re.match(version_regex, line))

setup(
    name="fastcli",
    version=__version__,
    description="Python3 CLI script for fast.com",
    long_description=readme + "\n\n" + history,
    author="Nathan Henrie",
    author_email="nate@n8henrie.com",
    url="https://github.com/n8henrie/fastcli",
    packages=find_packages('src'),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        'console_scripts': ['fastcli=fastcli.fastcli:cli']
        },
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords="fastcli",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ],
    extras_require={
        "dev": dev_requirements
        },
    test_suite="tests",
    tests_require=['pytest==3.0.4']
)
