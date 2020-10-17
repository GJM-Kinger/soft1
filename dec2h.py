# @todo
# @Author: gou
# @Time: 2020/9/22 21:44
# @version: 1.0
base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'), ord('A') + 6)]


def dec2hex(string_num):
    num1 = int(string_num)
    mid = []
    num = num1
    while True:
        if num == 0:
            mid.append('0')
            break
        num, rem = divmod(num, 16)
        mid.append(base[rem])
    if len(mid) % 2 != 0:
        mid.append('0')
    mid.append('0x')
    return ''.join([str(x) for x in mid[::-1]])


# 十六进制可以时间补充多余的零
def num_len(stringNum):
    num = dec2hex(stringNum)
    num_M = ''
    if num == '0x':
        num_M = '0x0000'
    else:
        if len(num) == 4:
            num_M += '0x00'
            num_M += num[2:]
        else:
            num_M += num
    return num_M


# 转化为16进制，位数是偶数，但是不会添加多余的零
def dec2hex1(string_num):
    num1 = int(string_num)
    mid = []
    num = num1
    while True:
        if num == 0:
            break
        num, rem = divmod(num, 16)
        mid.append(base[rem])
    if len(mid) % 2 != 0:
        mid.append('0')
    mid.append('0x')
    return ''.join([str(x) for x in mid[::-1]])


if __name__ == '__main__':
    str_h = num_len(37)
    print(str_h)
    print(dec2hex1(1))


    # print(num_len('1'))
    # num1 = '0x'
    # num2 = '0x'
    # num1 += num_M[4:]
    # num2 += num_M[2:4]
    # list_num = []
    # print(dec2hex('15'))



