import fileinput
import random
import copy


def find_possible_intersections(arr):
    ans = []
    for word_1 in range(len(arr)):
        for word_2 in range(word_1 + 1, len(arr)):
            for letter in range(len(arr[word_1])):
                if arr[word_1][letter] in arr[word_2]:
                    ans.append([word_1, word_2])
                    break
    return ans


def check_crossword(intersections_par, real_intersections_par=None):
    if not intersections_par:
        # print(real_intersections_par)
        return True
    intersections = copy.deepcopy(intersections_par)
    real_intersections = copy.deepcopy(real_intersections_par) if real_intersections_par is not None else []

    used = []
    for real_intersection in real_intersections:
        used.append([real_intersection[0], real_intersection[2]])
        used.append([real_intersection[1], real_intersection[3]])

    intersection = intersections[0]
    has_solution = False
    for letter_a in range(len(inp[intersection[0]])):
        for letter_b in range(len(inp[intersection[1]])):
            if inp[intersection[0]][letter_a] == inp[intersection[1]][letter_b]:
                # print(inp[intersection[0]], inp[intersection[1]])
                if [intersection[0], letter_a] not in used and [intersection[1], letter_b] not in used:
                    # add check crossword build
                    real_intersections.append([intersection[0], intersection[1], letter_a, letter_b])
                    has_solution += check_crossword(intersections[1:], real_intersections)
                    real_intersections.pop()
    # print(real_intersections)
    return has_solution


def choose_best_crosswords(crosswords_par, num_of_best=10):
    fitness_function = []

    def dfs(node):
        cnt = 0
        used[node] = True
        for destination in crossword:
            if destination[0] == node and not used[destination[1]]:
                cnt += dfs(destination[1])
            if destination[1] == node and not used[destination[0]]:
                cnt += dfs(destination[0])
        return cnt + 1

    for crossword in crosswords_par:
        used = [False] * n
        fitness = 0
        for vertex in range(n):
            if not used[vertex]:
                num = dfs(vertex)
                fitness += num * num
        fitness_function.append([fitness, len(fitness_function)])
    fitness_function.sort(key=lambda x: x[0], reverse=True)
    # check_crossword(crosswords[fitness_function[0][1]])
    # print(fitness_function[0][0])
    # print(crosswords[fitness_function[0][1]])
    best_crosswords_found = []
    for best_i in range(num_of_best):
        best_crosswords_found.append(crosswords[fitness_function[best_i][1]])
    return best_crosswords_found


def crosswords_crossover(crossword_a_par, crossword_b_par, longer):
    crossword_a = copy.deepcopy(crossword_a_par)
    crossword_b = copy.deepcopy(crossword_b_par)
    if len(crossword_b) > len(crossword_a):
        crossword_a, crossword_b = crossword_b, crossword_a

    separate_line = list(range(1, len(crossword_b)))
    while separate_line:
        i = random.choice(separate_line)
        separate_line.remove(i)
        crossover = []
        for j in range(i):
            crossover.append(crossword_b[j] if longer else crossword_a[j])
        for j in range(i, len(crossword_a if longer else crossword_b)):
            crossover.append(crossword_a[j] if longer else crossword_b[j])
        unique_crossover = []
        for intersection in crossover:
            if intersection not in unique_crossover:
                unique_crossover.append(intersection)
        if check_crossword(unique_crossover):
            return unique_crossover

    return crossword_a if random.random() <= 0.5 else crossword_b


inp = []
for line in fileinput.input(files='input.txt'):
    inp.append(line.removesuffix("\n"))
n = len(inp)
possible_intersections = find_possible_intersections(inp)
crosswords = []
# print(possible_intersections)
for i in range(100):
    while True:
        random_crossword = []
        temp_possible_intersections = copy.deepcopy(possible_intersections)
        while random.random() <= 0.66:
            if not temp_possible_intersections:
                break
            temp_intersection = random.choice(temp_possible_intersections)
            temp_possible_intersections.remove(temp_intersection)
            random_crossword.append(temp_intersection)
        if check_crossword(random_crossword):
            crosswords.append(random_crossword)
            break

while True:
    best_crosswords = choose_best_crosswords(crosswords)
    crosswords = copy.deepcopy(best_crosswords)
    for i in range(10):
        for j in range(i + 1, 10):
            crosswords.append(crosswords_crossover(best_crosswords[i], best_crosswords[j], True))
            crosswords.append(crosswords_crossover(best_crosswords[i], best_crosswords[j], False))
    print(len(crosswords))
