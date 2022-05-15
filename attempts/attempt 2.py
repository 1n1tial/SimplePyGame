# random
name = input("Enter your name: ")
age = input("Enter your age: ")
age_plus_one = int(age) + 1
if age_plus_one % 10 == 1:
    x = "st"
elif age_plus_one % 10 == 2:
    x = "nd"
elif age_plus_one % 10 == 3:
    x = "rd"
else:
    x = "th"
print("Hi " + name + ", nice to meet you!")
print("It appears that your " + str(age_plus_one) + x + " birthday is approaching!")
