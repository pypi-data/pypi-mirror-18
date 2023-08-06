#coding=utf-8

from setuptools import setup,find_packages

setup(
	name = "xjson",
	version = "0.1.5",
	keywords = ("json","parse","xpath","syntax"),
	description = "allow you parse a json file with xpath syntax",
	license = "MIT License",
	install_requires = [],
	author = "zhangTian",
	author_email = "hhczy1003@gmail.com",
	packages = find_packages(),
	#packages = ["xjson","ReadMe\\.rst"],
	platforms = "any",
	#github 或read_the_docs上的链接
	url = "https://github.com/hhczy/xjson",
	long_description = open("README.rst").read()
	)
