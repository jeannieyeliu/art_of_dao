

for 三角 in range(1,10):
    for 圆 in range(1,10):
        for 星 in range(1,10):
            a = 三角*10+星
            b = 圆
            c = 星*10+圆
            if(a-b==c and 三角!=圆 and 圆!=星 and 三角!=星):
                print(str(a)+" - "+str(b)+" = " +str(c))
