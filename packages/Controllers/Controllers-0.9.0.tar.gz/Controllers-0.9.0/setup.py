from setuptools import setup, Extension
import os

def sources(src):
	for path, folders, files in os.walk(src):
		for f in files:
			if f.endswith('.cpp'):
				yield os.path.join(path, f)

XboxController = Extension(
	name = 'Controllers.XboxController',
	include_dirs = ['XboxController'],
	sources = list(sources('XboxController')),
)

setup(
	name = 'Controllers',
	version = '0.9.0',
	packages = ['Controllers'],
	ext_modules = [XboxController],
)
