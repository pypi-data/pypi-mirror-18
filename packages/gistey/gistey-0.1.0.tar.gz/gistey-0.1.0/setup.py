from setuptools import setup

with open('requirements.txt') as req:
    dependencies = req.read().splitlines()

with open('README.md') as readme:
    long_description = readme.read()

if __name__ == "__main__":
    setup(
        name='gistey',
        version="0.1.0",
        description="Make GitHub gists from cmdline/terminal",
        author="Meet Mangukiya",
        author_email="meetmangukiya98@gmail.com",
        maintainer="Meet Mangukiya",
        maintainer_email=("meetmangukiya98@gmail.com", ),
        url="http://meetmangukiya.github.io",
        install_requires=dependencies,
        license='MIT',
        py_modules=['gistey', 'ArgumentParser'],
        entry_points = {
            'console_scripts': [
                'gistey=gistey:main'
            ]
        }
    )
