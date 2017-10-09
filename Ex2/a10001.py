#!/usr/bin/python
# -*- coding: UTF-8 -*-

from oracle import *
import sys
from random import randrange

data = "9F0B13944841A832B2421B9EAF6D9836813EC9D944A5C8347A7CA69AA34D8DC0DF70E343C4000A2AE35874CE75E64C31"

ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]     #密文的16进制分开存入列表
C = [ctext[:16], ctext[16:32], ctext[-16:]]                         #将密文分为3部分存入C
#print C
P = [[0] * 16, [0] * 16, [0] * 16]
IV = [[0] * 16, [0] * 16, [0] * 16]            #初始向量IV

Oracle_Connect()
for bi in range(2):                            #因为问题给出的密文仅可分成3块，故只需要计算两次即可
    b = 2 - bi
    for k in range(16):
        C1 = [C[b-1][:], C[b][:]]   #开始猜第二块经过加密器加密后的密文（即第三块密文的IV）
        pos = 15 - k
        for i in range(pos):
            C1[0][i] = 0
        for i in range(pos + 1, 16):           #当倒数n位的IV即15-k个IV确定时，IV确定部分使用补全数异或IV得到确定的密文
            C1[0][i] = (k + 1) ^ IV[b][i]
        ii = -1
        for i in range(256):
            C1[0][pos] = i                   #倒数第一个不确定IV的16进制数所在位置从0开始一次试，直到加密过后的密文补全位的数量等于补全位的值
            rc = Oracle_Send(C1[0][:] + C1[1][:], 2)#猜测的密文块发给服务器判断，若解密之后与明文相同则返回1
            #print rc
            if rc == 1:                        #若返回1，则可求出IV值与对应的明文
                ii = i
                break
        IV[b][pos] = ii ^ (k + 1)
        P[b][pos] = C[b-1][pos] ^ IV[b][pos]
        #print ii
        #print P[b][pos]
Oracle_Disconnect()
#print P[1]
#print P[2]
#P = [[0] * 16, [0] * 16, [0] * 16]
#P[1] = [89, 97, 121, 33, 32, 89, 111, 117, 32, 103, 101, 116, 32, 97, 110, 32]
#P[2] = [65, 46, 32, 61, 41, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]
text = []                                      #连接明文块1和明文块2
for x in P[1]:
    text.append(chr(x))
for x in P[2]:
    if(x == 11):
        break
    else:
        text.append(chr(x))
a = ""
print ("the text is: %s") % a.join(text)
