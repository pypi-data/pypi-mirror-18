

import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
"""

"""
def read(fname):
    """
    定义一个read方法，用来读取目录下的长描述
    我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
    你也可以不用这个方法，自己手动写内容即可，
    PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
NAME = "RSA_Tools"
"""
名字，一般放你包的名字即可
"""
 
PACKAGES = ["RSA_Tools",]
"""
包含的包，可以多个，这是一个列表
"""
 
DESCRIPTION = "this is a test package for analysing RSA."
"""
关于这个包的描述
"""
 
LONG_DESCRIPTION = read("README.txt")
"""
参见read方法说明
"""
 
KEYWORDS = "RSA"
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""
 
AUTHOR = "Chris New"
"""
"""
 
AUTHOR_EMAIL = "ncxhxgtg@mail.ustc.edu.cn"
"""
科大学生，科大的邮件地址
"""
URL = 'http://www.ustc.edu.cn'
 
VERSION = "1.0.2"

 
LICENSE = "MIT"

 
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)