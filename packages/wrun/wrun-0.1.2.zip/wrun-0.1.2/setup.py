from setuptools import setup


setup(
   name='wrun',
   version='0.1.2',
   description='Run Remote Windows Executables',
   license="MIT",
   author='Marco De Paoli',
   author_email='depaolim@gmail.com',
   url="https://github.com/depaolim/wrun",
   packages=['wrun'], # same as name
   install_requires=['configparser'], # external packages as dependencies
   scripts=['wrun_service.py']
)
