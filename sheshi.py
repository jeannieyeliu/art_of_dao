import random
from gua64 import gua64
# 揲蓍法
次数 = 50
爻 = [None] * 3
爻爻 = [None] * 6


def div4(x):
    a, b = divmod(x, 4)
    if b == 0:
        a -= 1
        b = 4
    if a < 0:
        a = 0
    return a, b


def 排卦(i, 大堆):
    print("-----第", i + 1, "根爻：----");
    print("第一步，分二：（", 大堆, "根，分两堆）")
    left = random.randint(2, 大堆)
    right = 大堆 - left
    print('左：', left, ", 右：", right)

    print("\n第二步，卦一：(选择一堆，抽出一根)")
    choice = random.choice(['left', 'right'])
    print('选择了' + choice)
    if choice == 'left':
        left -= 1;
        print('左边减1：', left)
    else:
        right -= 1;
        print('右边减1：', right)

    print('第二步之后：左：', left, ", 右：", right)

    print("\n第三步，揲蓍：(选择一堆，抽出一根)")

    leftA, leftB = div4(left)
    rightA, rightB = div4(right)
    print("左堆：", 4 * leftA, '根，剩下', leftB, '根')
    print("右堆：", 4 * rightA, '根，剩下', rightB, '根')

    print("第四步：归奇。（大堆合起来，小堆合起来）")
    groupA = leftA * 4 + rightA * 4
    groupB = leftB + rightB

    print("大堆：", groupA)
    print("小堆：", groupB)

    爻[i] = (groupA, groupB)
    return groupA

number = [None] * 6
mmap = {6: '太阴', 7: '阳', 8: '阴', 9: '太阳'}
nmap = {6: 0, 7: 1, 8: 0, 9: 1}
for i in range(6):
    起始 = 49
    第二遍起始 = 排卦(0, 起始)
    第三遍起始 = 排卦(1, 第二遍起始)
    最后 = 排卦(2, 第三遍起始)
    结果, _ = divmod(最后, 4)
    print("最终结果，第", i + 1, "次：", 结果, ',', mmap[结果], '爻')
    爻爻[i] = (结果, mmap[结果])
    number[i] = nmap[结果]
print(爻)
print(爻爻)
print('''
6阴爻，太阴
7阳爻
8阴爻
9阳爻，太阳
''')
m_heng = {6: '— — x 6 太阴', 7: '———   7 阳', 8: '— —   8 阴', 9: '——— o 9 太阳'}
for item in 爻爻:
    print(m_heng[item[0]])

# 计算上卦和下卦
print(number)
卦 = {0: '坤', 1: '艮', 2: '坎', 3: '巽', 4: '震', 5: '离', 6: '兑', 7: '乾'}
象 = {0: '地', 1: '山', 2: '水', 3: '风', 4: '雷', 5: '火', 6: '泽', 7: '天'}

上卦数 = number[0] + number[1]*2 +number[2]*4
下挂数 = number[3] + number[4]*2 +number[5]*4
print(卦[上卦数]+卦[下挂数]);
print(象[上卦数]+象[下挂数]);


print(gua64[象[上卦数]+象[下挂数]])
