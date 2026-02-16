x = 10
y = 20
t0 = y * 2
t1 = x + t0
z = t1
print z
t2 = z > 50
if t2 goto L0
goto L1
L0:
t3 = z - 50
result = t3
goto L2
L1:
t4 = z + 50
result = t4
L2:
print result
sum = 0
i = 1
L3:
t5 = i <= 5
if t5 goto L4
goto L5
L4:
t6 = sum + i
sum = t6
t7 = i + 1
i = t7
goto L3
L5:
print sum
t8 = x + y
t9 = z - 10
t10 = t8 * t9
t11 = t10 / 2
answer = t11
print answer
