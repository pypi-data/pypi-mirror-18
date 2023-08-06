"""
function getItem
para: list
"""

def getItem(info):
    for item in info:
        if isinstance(item,list):
            getItem(item)
        else:
            print(item)

def getItem2(info):
    for item in info:
        print(item+'!!!!!!!!!!')
    print('end....')


if __name__ == '__main__':
    info = ['abcd',12,'bcd',[1,2,3,4,['abc','bcd','efg',12]]]
    getItem(info)