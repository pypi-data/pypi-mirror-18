#coding=utf-8

from setuptools import setup,find_packages

setup(
	name = "xjson",
	version = "0.1.2",
	keywords = ("json","parse","xpath","syntax"),
	description = "allow you parse a json file with xpath syntax",
	license = "MIT License",
	install_requires = [],
	author = "zhangTian",
	author_email = "hhczy1003@gmail.com",
	#packages = find_packages(),
	packages = ["xjson"],
	platforms = "any"
	)
