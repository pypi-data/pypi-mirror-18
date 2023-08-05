# 项目：标准库函数
# 模块：调试模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-12 17:25

from functools import wraps
import logging
import sys
from .path import is_dev

__all__='decorator','trace','config_log','ensure','info','fprint'

info=logging.info

def decorator(decorator):
    def _decorator(func):
        @wraps(func)
        def __decorator(*args,**kwargs):
            return decorator(func,*args,**kwargs)
        return __decorator
    return _decorator

@decorator
def trace(func,*args,**kwargs):
    print('The function %s is called'%(func.__name__))
    print('With arguments %s %s'%(args,kwargs))
    result=func(*args,**kwargs)
    print('The result is %s'%(result))
    return result

def config_log(**kwargs):
    kwargs.setdefault('datefmt','%Y-%m-%d %H:%M:%S')
    kwargs.setdefault('format','%(levelname)-9s %(message)s')
    kwargs.setdefault('level',10 if is_dev() else 30)
    logging.basicConfig(**kwargs)

def ensure(cond,msg,level="error"):
    if not cond:
        getattr(logging,level)(msg)
        if level in ('error','critical','fatal'):
            raise Exception(msg)

def fprint(*args,sep=' ',end='\n',replace='',**kw):
    '''force print, used in Windows,解决打印GBK问题
    其中replace是遇无法打印字符的替代字符'''
    try:
        print(*args,sep=sep,end=end,**kw)
    except UnicodeEncodeError:
        s = sep.join(str(x) for x in args)
        for c in s:
            try:
                print(c,end='')
            except UnicodeEncodeError:
                print(replace, end='')
        print(end,end='')
