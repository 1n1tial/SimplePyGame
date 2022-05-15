p = float(input("Enter p: "))
n = float(input("Enter n: "))
Rone = float(input("Enter R1: "))
Rtwo = float(input("Enter R2: "))

j = (n-1)*(1/Rone - 1/Rtwo) - 1/p
i = 1/j

print(i)

m = -i/p

print(m)

if i > 0:
    print("R")
else:
    print("V")

if m > 0:
    print("NI")
else:
    print("I")

if i > 0:
    print("diff")
if i < 0:
    print("same")
