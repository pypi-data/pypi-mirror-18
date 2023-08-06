from setuptools import setup

setup(
    name='shortpath',
    version='1.0.2',
    description="Shortpath provides a small name for your long project paths.",
    keywords='shortpath',
    author='Gaurav Kumar',
    author_email='aavrug@gmail.com',
    url='https://github.com/aavrug/shortpath.git',
    packages=['shortpath'],
    install_requires=['click', 'os', 'pwd', 'random', 're'],
    scripts=['bin/shortpath'],
    license='MIT')