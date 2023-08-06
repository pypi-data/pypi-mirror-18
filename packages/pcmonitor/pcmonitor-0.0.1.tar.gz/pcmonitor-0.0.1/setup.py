from setuptools import setup

setup(
    name='pcmonitor',
    version='0.0.1',
    description='HTOP Python package',
    author='suchbeat',
    author_email='s.u.chbeat@gmail.com',
    url='https://github.com/suchbeat/pcmonitor.git',
    py_modules=['pcmonitor'],
    install_requires=['psutil'],
)
