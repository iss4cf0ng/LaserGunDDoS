from random import randint

def randInt():
    x = randint(1024, 9000)
    return x

def randIP():
    ip = '.'.join(map(str, (randint(0, 255) for _ in range(4))))
    return ip

def str2strls(data: str, spliter=','):
    return [_ for _ in data.split(spliter)]

def str2intls(data: str, spliter=','):
    return [int(_) for _ in str2strls(data)]

def randomStr(length: int):
    chars = 'abcdefghijklmnopqrstuvwxyz'
    chars = chars + chars.upper() + '0123456789'

    return ''.join([chars[randint(1, length % len(chars))] for _ in range(0, length)])