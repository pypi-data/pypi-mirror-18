from setuptools import setup, find_packages

setup(
    name='Flask-LoginManager',
    version='1.0.1',
    keywords = ('login', 'role'),
    description='Login Manager that supports multi-role, inspired by flask-login',
    license='Free',
    author='rain',
    author_email='rain@joymud.com',
    url='',
    platforms = 'flask',
    packages=['flask_loginmanager'],
    install_requires=['Flask']
)