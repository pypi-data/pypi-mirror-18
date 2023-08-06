# 从 Python 发布工具导入“setup”函数
from distutils.core import setup
# setup 函数提供了一些参数，需要将模块的元数据与 setup 函数的参数关联
setup(
    name = 'echo_nester',
    version = '1.0.0',
    py_modules = ['echo_nester'],
    author = 'echo',
    author_email = 'hhwei.procrastination@gmail.com',
    url = 'https://github.com/Breakingred',
    description = 'A simple printer of nested lists',)
