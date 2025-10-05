import random
from gua64 import gua64, gua_image
from write_history import write_history

number = [None] * 6
number_bian = [None] * 6
side = {0: '反', 1: '正'}
money = {3: 1, 1: 1, 2: 0, 0: 0}
yinyang = {0: '— — 阴', 1: '——— 阳'}
yao_map = {}
bianyao_count = 0
bian_nums = '';
for i in range(0, 6):
    a = random.choice([1, 0])
    b = random.choice([1, 0])
    c = random.choice([1, 0])
    number[i] = money[a + b + c];
    number_bian[i] = money[a + b + c];
    bianyao = ""
    if a == b == c:
        bianyao = " O" if a == 1 else " X"
        bianyao_count += 1
        number_bian[i] = 0 if a == 1 else 1
        bian_nums += str(i+1) + "，"
    msg = '第' + str(i + 1) + '爻：' + side[a] + side[b] + side[c] + ', ' + yinyang[number[i]] + bianyao
    # print('第', i + 1, '爻：' + side[a] + side[b] + side[c] + ', ' + yinyang[number[i]] + bianyao)

    yao_map[i + 1] = {'msg': msg}

for i in range(6, 0, -1):
    print(yao_map[i]['msg'])

print(number)
卦 = {0: '坤', 1: '艮', 2: '坎', 3: '巽', 4: '震', 5: '离', 6: '兑', 7: '乾'}
象 = {0: '地', 1: '山', 2: '水', 3: '风', 4: '雷', 5: '火', 6: '泽', 7: '天'}

上卦数 = number[5] + number[4] * 2 + number[3] * 4
下挂数 = number[2] + number[1] * 2 + number[0] * 4
print(卦[上卦数] + 卦[下挂数]);
print(象[上卦数] + 象[下挂数]);

result = gua64[象[上卦数] + 象[下挂数]]
print(result)
write_history(result + " 变爻：" +bian_nums)

if (bianyao_count < 3):
    exit(0)
上卦数2 = number_bian[5] + number_bian[4] * 2 + number_bian[3] * 4
下挂数2 = number_bian[2] + number_bian[1] * 2 + number_bian[0] * 4
print('变卦：')
bian_result = gua64[象[上卦数2] + 象[下挂数2]]
print(bian_result)
write_history("    变卦："+bian_result)

