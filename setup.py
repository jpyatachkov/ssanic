from setuptools import setup

import ssanic

setup(
    name='ssanic',
    version=ssanic.__version__,
    packages=[
        'ssanic',
        'ssanic.http',
        'ssanic.http.response',
        'ssanic.parser',
        'ssanic.parser.config',
        'ssanic.parser.request'
    ],
    install_requires=[
        'uvloop',
    ],
    entry_points={
        'console_scripts': [
            'ssanic = ssanic.__main__:_main'
        ]
    },
    url='https://github.com/jpyatachkov/ssanic',
    license='MIT',
    author='jpyatachkov',
    author_email='cvkucherov@yandex.ru',
    description='Dummy implementation of web server that can only handle GET and HEAD requests'
)
