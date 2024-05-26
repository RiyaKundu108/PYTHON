def find_common_elements(list1, list2):
    return set(list1) & set(list2)

list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
print(find_common_elements(list1, list2))
