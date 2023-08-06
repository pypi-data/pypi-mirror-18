# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
      name='feiwu',   #名称
      version='0.0.2',  #版本
      description="some useful module on flask developer", #描述
      keywords='web flask',
      author='chen',  #作者
      author_email='chenyehai737@qq.com', #作者邮箱
      license = 'MIT',
      url='', #作者链接
      packages=['feiwu'],
      package_data={
        'feiwu': ['ipcool', 'provinces.json'],
      },
      zip_safe=False,
      classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],
      install_requires=[      #需求的第三方模块
        'Flask==0.10.1',
        'requests==2.7.0',
        'ujson==1.33',
        'qiniu==7.0.4',
      ],
      entry_points={
      },
)

