in_num = int(input('Enter the input number: '))
not1 = int(input('Enter the current base: '))
not2 = int(input('Enter the base of the output: '))

orig_array = [int(a) for a in str(in_num)]
orig_num = 0

for i in range(len(orig_array)):
    orig_num += (not1 ** i) * orig_array[-i - 1]

result_array = []
while orig_num > 0:
    result_array.append(orig_num % not2)
    orig_num //= not2

result_array.reverse()

result_array = [str(num) for num in result_array]
result = "".join(result_array)
print(int(result))




