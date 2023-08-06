from setuptools import setup
import setuptools, tokenize
setup(
	name='cis-jarvis',# This is the name of your PyPI-package.
	version='0.13',   # Update the version number for new releases
	scripts=['jarvis/jarvis.py']# The name of your scipt, and also the command you'll be using for calling it
 )

install_requires = [
    'PyAudio',
    'SpeechRecognition',
],