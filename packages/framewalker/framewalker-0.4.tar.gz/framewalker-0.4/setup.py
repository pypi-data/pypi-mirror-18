from setuptools import setup

setup(
    name='framewalker',
    version='0.4',
    url='https://github.com/stefanbie/FrameWalker',
    install_requires=[
        'peewee',
        'PyMySQL',
    ],
    py_modules=['Timings','IFrame', 'JavaScript','DB']
    )
