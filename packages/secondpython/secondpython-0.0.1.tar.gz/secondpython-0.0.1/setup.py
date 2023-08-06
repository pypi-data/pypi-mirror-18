# -*- coding: utf-8 -*-

from setuptools import setup

f = open("README.md")
long_description = f.read()

setup(
    name = 'secondpython',                                  # 包名
    version = '0.0.1',                                      # 版本号
    keywords = ('hello', 'python', 'pypi', 'second'),       # 关键词，在pypi搜索是很起作用，可以多写点
    description = 'second pypi',                            # 单行描述，不能超过200个字符
    long_description = long_description,                    # 多行描述，可以很多，所以写到另一文件，一般写包的用法，修改日志等等
    license = 'MIT License',                                
    install_requires = ['simplejson>=1.1'],                 # 依赖包及其版本，此次我是随便写的
    author = 'andyron',                                     # 作者
    author_email = 'randy.njfu@gmail.com',                  
    maintainer = 'andyron',                                 # 维护者
    maintainer_email = 'randy.njfu@gmail.com',              
    url = 'https://github.com/andyRon/secondpython',        
    download_url = 'https://github.com/andyRon/secondpython',
    
    platforms = [2.7, 3.5, 3.6],                            # python的版本

    classifiers = [                                         # 包的分类，便于在pypi搜索
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Bug Tracking',
    ]
)