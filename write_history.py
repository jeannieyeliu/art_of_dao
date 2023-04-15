import time


def write_history(gua):
    current_time = time.localtime()
    file = open('gua_history.txt', 'a');
    year = current_time.tm_year
    month = current_time.tm_mon
    day = current_time.tm_mday
    hour = current_time.tm_hour
    min = current_time.tm_min
    sec = current_time.tm_sec

    file.writelines("{}-{}-{} {}:{}:{}, {}\n".format(year, month, day, hour,min,sec, gua));
    file.close();

# if __name__ == 'main':
# write_history('风天小畜')
