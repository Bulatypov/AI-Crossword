import fileinput
import random

answer = []
final_map = []
left = 0
up = 0


def solve_crossword(inp, test_num):
    global answer
    global final_map
    global left
    global up

    def find_possible_intersections(arr):
        ans = []
        for word_1 in range(len(arr)):
            for word_2 in range(word_1 + 1, len(arr)):
                for letter in range(len(arr[word_1])):
                    if arr[word_1][letter] in arr[word_2]:
                        ans.append([word_1, word_2])
                        break
        return ans

    def check_crossword_build(real_intersections_par):
        global answer
        global final_map
        map_crossword = [['.' for _ in range(100)] for _ in range(100)]
        if not real_intersections_par or len(real_intersections_par) == 1:
            final_map = map_crossword[:]
            return True
        real_intersections = real_intersections_par[:]
        num_crossword = [[[] for _ in range(100)] for _ in range(100)]
        placed_words = [[real_intersections[0][0], 50, 50, True]]
        used_words = [False] * n
        used_words[real_intersections[0][0]] = True

        def place_word(word, row, column, vertical):
            current_word_num = len(placed_words) - 1

            def is_start(word_ind, x_coord, y_coord):
                return placed_words[word_ind][1] == x_coord and placed_words[word_ind][2] == y_coord

            def is_finish(word_ind, x_coord, y_coord):
                return (placed_words[word_ind][1] + (len(inp[placed_words[word_ind][0]]) - 1) *
                        placed_words[word_ind][3] == x_coord and
                        placed_words[word_ind][2] + (len(inp[placed_words[word_ind][0]]) - 1) *
                        (not placed_words[word_ind][3]) == y_coord)

            letter_ind = 0
            for x in range(row, row + (len(word) - 1) * vertical + 1):
                for y in range(column, column + (len(word) - 1) * (not vertical) + 1):
                    if map_crossword[x][y] == '.' or map_crossword[x][y] == word[letter_ind]:
                        map_crossword[x][y] = word[letter_ind]
                        num_crossword[x][y].append(current_word_num)
                        letter_ind += 1
                    else:
                        return False

            for x in range(row, row + (len(word) - 1) * vertical + 1):
                for y in range(column, column + (len(word) - 1) * (not vertical) + 1):
                    neighbours = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
                    for neighbour in neighbours:
                        n_x = neighbour[0]
                        n_y = neighbour[1]
                        if num_crossword[n_x][n_y] == num_crossword[x][y] or not num_crossword[n_x][n_y]:
                            continue
                        elif len(num_crossword[n_x][n_y]) > 2 or len(num_crossword[x][y]) > 2:
                            return False
                        elif list(set(num_crossword[x][y]) & set(num_crossword[n_x][n_y])):
                            all_words = num_crossword[x][y][:]
                            for neighbour_word in num_crossword[n_x][n_y]:
                                if neighbour_word not in all_words:
                                    all_words.append(neighbour_word)
                            if len(all_words) == 2:
                                if placed_words[all_words[0]][3] == placed_words[all_words[1]][3]:
                                    return False
                            elif len(all_words) == 3:
                                all_words = list(
                                    set(all_words) - (set(num_crossword[x][y]) & set(num_crossword[n_x][n_y])))
                                first = all_words[0]
                                second = all_words[1]
                                if first != current_word_num:
                                    first, second = second, first
                                if not (
                                        (is_start(first, x, y) and is_finish(second, n_x, n_y) or is_start(second, n_x,
                                                                                                           n_y)
                                         and is_finish(first, x, y))):
                                    return False
                        else:
                            return False
            return map_crossword

        place_word(inp[real_intersections[0][0]], 50, 50, True)

        while real_intersections:
            found_connection = False
            for real_intersection in real_intersections:
                if used_words[real_intersection[0]] and used_words[real_intersection[1]]:
                    return False
                if used_words[real_intersection[0]] and not used_words[real_intersection[1]]:
                    found_connection = True
                    for placed_word in placed_words:
                        if placed_word[0] == real_intersection[0]:
                            row_axis = placed_word[1] + (
                                real_intersection[2] if placed_word[3] else -real_intersection[3])
                            column_axis = placed_word[2] + (
                                -real_intersection[3] if placed_word[3] else real_intersection[2])
                            placed_words.append([real_intersection[1], row_axis, column_axis, not placed_word[3]])
                            used_words[real_intersection[1]] = True
                            if not place_word(inp[real_intersection[1]], row_axis, column_axis, not placed_word[3]):
                                return False
                            break
                    real_intersections.remove(real_intersection)
                    break

                elif used_words[real_intersection[1]] and not used_words[real_intersection[0]]:
                    for placed_word in placed_words:
                        if placed_word[0] == real_intersection[1]:
                            found_connection = True
                            row_axis = placed_word[1] + (
                                real_intersection[3] if placed_word[3] else -real_intersection[2])
                            column_axis = placed_word[2] + (
                                -real_intersection[2] if placed_word[3] else real_intersection[3])
                            placed_words.append([real_intersection[0], row_axis, column_axis, not placed_word[3]])
                            used_words[real_intersection[0]] = True
                            if not place_word(inp[real_intersection[0]], row_axis, column_axis, not placed_word[3]):
                                return False
                            break
                    real_intersections.remove(real_intersection)
                    break

            if not found_connection:
                map_crossword = [['.' for _ in range(100)] for _ in range(100)]
                num_crossword = [[[] for _ in range(100)] for _ in range(100)]
                placed_words = [[real_intersections[0][0], 50, 50, True]]
                used_words[real_intersections[0][0]] = True
        final_map = map_crossword[:]
        answer = placed_words[:]
        return True

    def check_crossword(intersections_par, real_intersections_par=None, printable=False):
        if not intersections_par:
            if not check_crossword_build(real_intersections_par):
                return False
            global final_map
            left_index = 100
            right_index = 0
            up_index = 100
            down_index = 0
            for i in range(100):
                for j in range(100):
                    if final_map[i][j] != '.':
                        left_index = min(left_index, j)
                        right_index = max(right_index, j)
                        up_index = min(up_index, i)
                        down_index = max(down_index, i)
            if right_index - left_index > 19 or down_index - up_index > 19:
                return False
            if printable:
                res_crossword = [['.' for _ in range(20)] for _ in range(20)]
                for i in range(up_index, down_index + 1):
                    for j in range(left_index, right_index + 1):
                        res_crossword[i - up_index][j - left_index] = final_map[i][j]
                for i in res_crossword:
                    for j in i:
                        print(j, end=' ')
                    print()
            global left
            global up
            if len(answer) == n:
                left = left_index
                up = up_index
            return True

        real_intersections = real_intersections_par[:] if real_intersections_par else []
        used = []
        for real_intersection in real_intersections:
            used.append([real_intersection[0], real_intersection[2]])
            used.append([real_intersection[1], real_intersection[3]])

        intersection = intersections_par[0]
        for letter_a in range(len(inp[intersection[0]])):
            for letter_b in range(len(inp[intersection[1]])):
                if inp[intersection[0]][letter_a] == inp[intersection[1]][letter_b]:
                    if [intersection[0], letter_a] not in used and [intersection[1], letter_b] not in used:
                        real_intersections.append([intersection[0], intersection[1], letter_a, letter_b])
                        if check_crossword(intersections_par[1:], real_intersections, printable):
                            return True
                        real_intersections.pop()
        return False

    def choose_best_crosswords(crosswords_par, num_of_best):
        fitness_function = []

        def dfs(node):
            cnt = 1
            used[node] = True
            for destination in crossword:
                if destination[0] == node and not used[destination[1]]:
                    cnt += dfs(destination[1])
                if destination[1] == node and not used[destination[0]]:
                    cnt += dfs(destination[0])
            return cnt

        for crossword in crosswords_par:
            used = [False] * n
            fitness = 0
            for vertex in range(n):
                if not used[vertex]:
                    num = dfs(vertex)
                    fitness += num * num
            fitness_function.append([fitness, len(fitness_function)])
        fitness_function.sort(key=lambda x: x[0], reverse=True)
        best_crosswords_found = []
        for best_i in range(num_of_best):
            best_crosswords_found.append(crosswords[fitness_function[best_i][1]])
        return best_crosswords_found

    def crosswords_crossover(crossword_a_par, crossword_b_par, longer):
        crossword_a = crossword_a_par[:]
        crossword_b = crossword_b_par[:]
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
            return unique_crossover
        return crossword_a if random.random() <= 0.5 else crossword_b

    def crosswords_mutation(initial_crosswords):
        res_crosswords = []
        for crossword in initial_crosswords:
            proper_crossword = False
            possible_mutations = [elem for elem in possible_intersections if elem not in crossword]
            swap_mutations = [elem for elem in possible_intersections if elem not in crossword]
            while not proper_crossword:
                random_choice = random.random()
                if random_choice <= 0.25 and crossword:
                    crossword.remove(random.choice(crossword))
                    break
                elif random_choice <= 0.5:
                    while possible_mutations:
                        new_intersection = random.choice(possible_mutations)
                        possible_mutations.remove(new_intersection)
                        crossword.append(new_intersection)
                        if check_crossword(crossword):
                            proper_crossword = True
                            if len(answer) == n:
                                return res_crosswords
                            break
                        else:
                            crossword.pop()
                            if random.random() <= 0.1:
                                break
                elif random_choice <= 0.75 and crossword:
                    random_ind = random.randint(0, len(crossword) - 1)
                    while possible_mutations:
                        new_intersection = random.choice(swap_mutations)
                        crossword[random_ind] = new_intersection
                        if check_crossword(crossword):
                            proper_crossword = True
                            if len(answer) == n:
                                return res_crosswords
                            break
                        else:
                            if random.random() <= 0.3:
                                crossword.pop(random_ind)
                                proper_crossword = True
                                break
                else:
                    break
            res_crosswords.append(crossword)
        return res_crosswords

    def print_answer():
        final_answer = [[]] * n
        for i in answer:
            final_answer[i[0]] = [i[1] - up, i[2] - left, int(i[3])]
        with open(f"outputs/output{test_num}.txt", "w") as output:
            for row in final_answer:
                output.write(" ".join(map(str, row)) + "\n")

    n = len(inp)
    possible_intersections = find_possible_intersections(inp)
    crosswords = []
    for i in range(n * n):
        crosswords.append([])

    loop_cnt = 0
    while True:
        if loop_cnt >= 100:
            return False
        if len(answer) == n:
            print_answer()
            return True
        best_crosswords = choose_best_crosswords(crosswords, n)
        crosswords = best_crosswords[:]
        for i in range(n):
            for j in range(i + 1, n):
                crosswords.append(crosswords_crossover(best_crosswords[i], best_crosswords[j], True))
                crosswords.append(crosswords_crossover(best_crosswords[i], best_crosswords[j], False))
        crosswords = crosswords_mutation(crosswords)
        loop_cnt += 1


for test_number in range(1, 101):
    input_words = []
    answer = []
    final_map = []
    left = 0
    up = 0
    for line in fileinput.input(files=f'inputs/input{test_number}.txt'):
        input_words.append(line.removesuffix("\n"))
    while not solve_crossword(input_words, test_number):
        print("Reboot!")
