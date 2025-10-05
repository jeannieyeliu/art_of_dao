import time
import os


def write_history(gua):
    current_time = time.localtime()
    
    # Ensure Gua_history directory exists
    if not os.path.exists('Gua_result'):
        os.makedirs('Gua_result')
    
    file_path = os.path.join('Gua_result', 'gua_history.txt')
    with open(file_path, 'a') as file:
        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        hour = current_time.tm_hour
        min = current_time.tm_min
        sec = current_time.tm_sec

        file.write("{}-{}-{} {}:{}:{}, {}\n".format(year, month, day, hour, min, sec, gua))

# if __name__ == 'main':
#     write_history('风天小畜')
