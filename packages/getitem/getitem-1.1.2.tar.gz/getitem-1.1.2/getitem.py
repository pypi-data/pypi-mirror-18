"""
function getItem
para: list
"""

def getItem(info,isIndent=False,level=0):
    for item in info:
        if isinstance(item,list):
            getItem(item,isIndent,level+1)
        else:
            if isIndent:
                print('-'*level+str(item))
            else:
                print(str(item))

def getItem2(info):
    for item in info:
        print(item+'!!!!!!!!!!')
    print('end....')


if __name__ == '__main__':
    info = ['abcd',[12,13,14,15],'bcd',[1,2,3,4,['abc','bcd','efg',12]]]
    getItem(info)