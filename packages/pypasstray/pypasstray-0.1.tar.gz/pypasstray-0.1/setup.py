try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

setup(
        name='pypasstray',
        version='0.1',
        author='Ozan Safi',
        author_email='ozansafi@gmail.com',
        py_modules=['pypasstray'],
        scripts=['pypasstray.py'],
        url='https://github.com/ozans/pypasstray',
        description='A simple GTK3 system tray indicator for the UNIX password manager (pass)',
        install_requires=[],
)
