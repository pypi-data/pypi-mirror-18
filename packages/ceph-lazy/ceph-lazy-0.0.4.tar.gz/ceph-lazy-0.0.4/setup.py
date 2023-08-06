#encoding:utf-8
from setuptools import setup, find_packages
import sys, os

version = '0.0.4'

setup(name='ceph-lazy',
      version=version,
      py_modules=['ceph-lazy'],
      description="ceph cmd tool to lazy",
      long_description="""ceph cmd tool to lazy""",
      classifiers=[],
      keywords='python ceph lazy',
      author='zphj1987',
      author_email='199383004@qq.com',
      url='https://github.com/zphj1987/ceph-lazy/tree/lazy-python',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'requests',
      ],
#      entry_points={
#        'console_scripts':[
#           'ceph-lazy = ceph-lazy:main'
#        ]
#      },
)
