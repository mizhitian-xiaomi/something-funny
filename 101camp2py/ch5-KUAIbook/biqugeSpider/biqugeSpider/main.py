'''as main action script demo
'''
__author__ = '101camp2py'
__version__ = 'v190907.2142'

# main.py在biqugeSpider目录下时用这个
from spiders import biquge as sb

# main.py在spiders目录下时用这个
# import biquge as sb


def main():
    '''test import sub mod.class
    '''
    sbb = sb.BiqugeSpider()
    print(type(sbb))
    return None

if __name__ == '__main__':
    '''test import relation
    '''
    print(__author__)
    print(__version__)
    main()

'''
运行应该获得:

༄  python main.py
101camp2py
v190907.2142
<class 'spiders.biquge.BiqugeSpider'>

'''