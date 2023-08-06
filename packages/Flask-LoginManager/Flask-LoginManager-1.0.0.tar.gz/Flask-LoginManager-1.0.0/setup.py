from setuptools import setup, find_packages

setup(
    name='Flask-LoginManager',
    version='1.0.0',
    keywords = ('login', 'role'),
    description='Login Manager that supports multi-role, inspired by flask-login',
    license='Free',
    author='rain',
    author_email='rain@joymud.com',
    url='',
    platforms = 'flask',
    packages = find_packages('./app/loginmanager'),
    setup_requires=['flask>=0.11.1'],
)