import fileinput
import math

import numpy
import matplotlib.pyplot as plt

mean_arr = numpy.array([])
max_arr = numpy.array([])
num = [[]] * 100

for test_number in range(1, 101):
    for line in fileinput.input(files=f'statistics/stat{test_number}.txt'):
        if "Average" in line:
            mean_arr = numpy.append(mean_arr, float(line.split(': ')[1]))
        else:
            max_arr = numpy.append(max_arr, float(line.split(': ')[1]))
            num[int(math.sqrt(max_arr[-1]))].append(mean_arr[-1])

ans = []
for i in num:
    if sum(i) > 0:
        ans.append(sum(i) / len(i))
print(len(ans))
# print("Mean:", round(fitness_arr.mean(), 2))
# print("Maximum:", sorted(fitness_arr)[-1])

# print("Mean: ", mean_arr)
# print("Maximum: ", max_arr)
#
# x = [i for i in range(5, 20)]
# y = sorted(ans)

# plt.plot(x, y)
#
# plt.show()
# def generation_imitation(inp, test_num):
#     with open(f"statistics/stat{test_num}.txt", "w") as output:
#         output.write(f"Average fitness function: {(len(inp) / 2)**2 + random.randint(math.floor(random.choice([len(inp) / 2, math.ceil(len(inp) / 2)])), math.floor(len(inp) / 2 * 3))}\n")
#         output.write(f"Maximum fitness function: {len(inp)**2}")
