a = 10
b = 20
t1 = b * 2
t2 = a + t1
c = t2
d = 14
t3 = a < b
ifFalse t3 goto L1
max_val = b
goto L2
L1:
max_val = a
L2:
count = 0
L3:
t4 = count < 5
ifFalse t4 goto L4
t5 = count + 1
count = t5
goto L3
L4:
sum = 0
i = 1
L5:
t6 = i <= 10
ifFalse t6 goto L6
t7 = sum + i
sum = t7
i = i + 1
goto L5
L6:
func calculate_area():
t8 = width * height
area = t8
return area
endfunc
result = 100
return result
