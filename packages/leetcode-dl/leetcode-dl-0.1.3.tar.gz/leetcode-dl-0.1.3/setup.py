from setuptools import setup
from codecs import open

name = "leetcode-dl"
packages = [
    "leetcode_dl",
    "leetcode_dl_cli"
]

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name=name,
    version="0.1.3",
    keywords="leetcode download",
    description="Command-line program to download solutions from leetcode.com",
    download_url="https://pypi.python.org/pypi/{}".format(name),
    long_description=readme,
    license="MIT License",
    url='http://github.com/bonfy/{}'.format(name),
    author="bonfy",
    author_email="foreverbonfy@163.com",
    install_requires=[
        "requests",
        "clint",
        "pyquery"
    ],
    packages=packages,
    entry_points={"console_scripts": "leetcode-dl=leetcode_dl_cli.main:main"},
    platforms="any",
    # classifiers=(
    #     'Development Status :: 4 - Beta',
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.3',
    #     'Programming Language :: Python :: 3.4',
    #     'Programming Language :: Python :: 3.5'
    # ),
)
