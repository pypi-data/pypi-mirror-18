# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
      name='fw_test',   #名称
      version='0.0.1',  #版本
      description="test the packages upload", #描述
      keywords='test flask',
      author='chen',  #作者
      author_email='chenyehai737@qq.com', #作者邮箱
      license = 'MIT',
      url='', #作者链接
      packages=find_packages(exclude=['flask_request']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[      #需求的第三方模块
        'requests',
      ],
      entry_points={
      },
)

