

from setuptools import setup, find_packages


setup(name='Analyzer-zero',
    version='0.1',
    description='a anayzer package',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['mroylib-min','jieba', 'bs4','pandas', 'SciPy' ,'Pillow'],

)


