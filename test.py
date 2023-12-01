list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 8, 7]

all_elements = list1[:]
for elem in list2:
    if elem not in all_elements:
        all_elements.append(elem)
print(all_elements)
common_elements = list(set(list1) & set(list2))
print(common_elements)
print(list(set(all_elements) - set(common_elements)))
