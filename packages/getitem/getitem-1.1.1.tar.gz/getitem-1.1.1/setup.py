from distutils.core import setup

"""
https://pypi.python.org注册账号密码
username:deyangcai
password:cwq926823926823,.

python setup.py sdist
python setup.py install
python setup.py register

"""

setup(
    name = 'getitem',
    version = '1.1.1',
    py_modules = ['getitem'],
    author = 'Caideyang',
    author_email = 'deyangcai@163.com',
    url = 'https://www.baidu.com',
    description = 'get items of a list '
)