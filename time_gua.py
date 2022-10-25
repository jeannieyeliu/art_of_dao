# 按时间起卦
from gua64 import gua64, gua_image
import time
from zhdate import datetime
from zhdate import ZhDate
from math import ceil

dizhi_map = {1: '子', 2: '丑', 3: '寅', 4: '卯', 5: '辰', 6: '巳', 7: '午', 8: '未', 9: '申', 10: '酉', 11: '戌', 12: '亥', }
gua_map = {1: '天', 2: '泽', 3: '火', 4: '雷', 5: '风', 6: '水', 7: '山', 8: '地'}
卦 = {0: '坤', 1: '艮', 2: '坎', 3: '巽', 4: '震', 5: '离', 6: '兑', 7: '乾'}
象 = {0: '地', 1: '山', 2: '水', 3: '风', 4: '雷', 5: '火', 6: '泽', 7: '天'}


def moder(num, mod_by):
    result = num % mod_by
    if result == 0:
        result = mod_by
    return result


def calc_change_gua(上卦数, 下卦数, 动爻数):
    用下卦 = True
    用卦数 = 下卦数
    if 动爻数 >= 4:
        用下卦 = False
        用卦数 = 上卦数
        动爻数 -= 3
    if 动爻数 == 3:
        动爻数 = 1
    elif 动爻数 == 1:
        动爻数 = 4
    num = 8 - 用卦数;
    num = num ^ 动爻数
    变卦数 = 8 - num
    if 用下卦:
        return 上卦数, 变卦数
    else:
        return 变卦数, 下卦数


def lunar_h(hour):
    return ceil(hour / 2) + 1


# 获取当前时间：
current_time = time.localtime()
year = current_time.tm_year
month = current_time.tm_mon
day = current_time.tm_mday
hour = current_time.tm_hour

lunar_date = ZhDate.from_datetime(datetime(year, month, day))
print(lunar_date)
# 计算地支年数

lunar_year = lunar_date.lunar_year
lunar_day = lunar_date.lunar_day
lunar_month = lunar_date.lunar_month
lunar_hour = lunar_h(hour)

dizhi_num = moder((lunar_year - 1911), 12)
if dizhi_num == 0: dizhi_num = 12
print('年支数：', dizhi_num, dizhi_map[dizhi_num])
print('月数:', lunar_month)
print('日数：', lunar_day)
print('时辰数：', lunar_hour, dizhi_map[lunar_hour])

up_gua_num = moder(dizhi_num + lunar_month + lunar_day, 8)
down_gua_num = moder(dizhi_num + lunar_month + lunar_day + lunar_hour, 8)
move_yao_num = moder(dizhi_num + lunar_month + lunar_day + lunar_hour, 6)

up_gua = gua_map[up_gua_num]
down_gua = gua_map[down_gua_num]
move_yao = gua_map[move_yao_num]
up_gua_img = gua_image[up_gua_num]
down_gua_img = gua_image[down_gua_num]

move_gua_img = gua_image[move_yao_num]

up_change_gua_num, down_change_gua_num = calc_change_gua(up_gua_num, down_gua_num, move_yao_num)
up_change_gua = gua_map[up_change_gua_num]
down_change_gua = gua_map[down_change_gua_num]
up_change_gua_img = gua_image[up_change_gua_num]
down_change_gua_img = gua_image[down_change_gua_num]

print('上卦', up_gua_num, up_gua, up_gua_img)
print('下卦', down_gua_num, down_gua, down_gua_img)
print('本卦', gua64[up_gua + down_gua])
print('——————————————')
print('动爻', move_yao_num, move_yao, move_gua_img)
print('——————————————')
print('上变卦', up_change_gua_num, up_change_gua, up_change_gua_img)
print('下变卦', down_change_gua_num, down_change_gua, down_change_gua_img)
print('变卦', gua64[up_change_gua + down_change_gua])
