"""Setup.py file for atemon.EmailValidator package."""
from distutils.core import setup

setup(
    name='Atemon-EmailValidator',
    version='0.1.1.2',
    packages=['atemon', 'atemon.EmailValidator'],
    long_description="Email validator for Python",
    author="Varghese Chacko",
    author_email="varghese@atemon.com",
    url="https://github.com/atemon/python-sms-api",
    provides=["EmailValidator"],
    license="MIT License",
)
