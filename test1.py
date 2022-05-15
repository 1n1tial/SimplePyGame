# n = int(input())
# dic = {}
# li = []
# for i in range(n):
#     a, b = map(int, input().split())
#     dic[a] = b
#     li.append(a)
# li.sort()
# for a in li:
#     print(a, dic[a])

# n = int(input())
# score_list = list(map(int, input().split()))
# newlist = list(reversed(sorted(score_list)))
# # print(newlist)
# place_list = []
# for i in range(n):
#     a = 0
#     for j in range(i):
#         if newlist[j] > newlist[i]:
#             a += 1
#     place_list.append(a+1)
#     # print(place_list)
#
# dic = dict(zip(newlist, place_list))
# # print(dic)
# for score in score_list:
#     print(score, dic[score])


# people_list = []
# people = 0
# for i in range(10):
#     a, b = map(int, input().split())
#     people += b
#     people -= a
#     people_list.append(people)
# print(max(people_list))


# a, b, c, d, e, f, g = map(int, input().split())
# lottery = {a, b, c, d, e, f}
# bonus = g
# jihye = set(map(int, input().split()))
# andset = lottery & jihye
# if len(andset) == 6:
#     print(1)
# elif len(andset) == 5 and bonus in jihye:
#     print(2)
# elif len(andset) == 5:
#     print(3)
# elif len(andset) == 4:
#     print(4)
# elif len(andset) == 3:
#     print(5)
# else:
#     print(0)


# a = int(input())
# set1 = set(map(int, input().split()))
# b = int(input())
# set2 = set(map(int, input().split()))
#
# if len(set1 & set2) != 0:
#     for i in sorted(list(set1 & set2)):
#         print(i, end=' ')
# else:
#     print(0, end='')
# print()
# for i in sorted(list(set1 | set2)):
#     print(i, end=' ')


def foo(b):
    b[0] = 1
    b = [5, 2, 0]
    b[0] = 45

a = [3, 2, 1]
foo(a)
print(a)




