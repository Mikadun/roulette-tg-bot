from random import randint

def classic(players):
    even, odd, red, black, L, H = [],[],[],[],[],[]
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    for i in range(1, 37):
        if i%2 == 0:
            even.append(i)
        else:
            odd.append(i)
        if i<=18:
            L.append(i)
        else:
            H.append(i)
        if i not in red:
            black.append(i)
    x = randint(0, 36)
    print(x)
    res = {}
    for i in players:
        if res.get(i[0]) == None:
            res[i[0]] = 0
        if i[1] == 'Even' and x in even:
            res[i[0]] += int(i[2])*2
        elif i[1] == 'Odd' and x in odd:
            res[i[0]] += int(i[2])*2
        elif i[1] == 'Red' and x in red:
            res[i[0]] += int(i[2])*2
        elif i[1] == 'Black' and x in black:
            res[i[0]] += int(i[2])*2
        elif i[1] == '1-18' and x in L:
            res[i[0]] += int(i[2])*2
        elif i[1] == '19-36' and x in H:
            res[i[0]] += int(i[2])*2
        elif int(i[1]) == x:
            res[i[0]] += int(i[2])*36
    return res 