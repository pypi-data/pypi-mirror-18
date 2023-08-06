from setuptools import setup, find_packages

setup(
    name='set-fns',
    version='0.1.1',
    packages=find_packages(),
    scripts=['set-fns'],
    author='Yamil Asusta (@elbuo8)',
    author_email='hello@yamilasusta.com',
    license='MIT',
    description='Quick set operations on files',
    keywords='union intersection difference set sets discrete math',
    url='https://github.com/elbuo8/set-fns',
    long_description=open('./README.md').read(),
)
