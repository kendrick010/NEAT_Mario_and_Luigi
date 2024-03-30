from collections import Counter

def most_occuring_element(lst):
    frequencies = Counter(lst)
    return max(frequencies, key=frequencies.get)


# Example usage:
my_list = [1, 2, 3, 4, 1, 2, 2, 3, 1, 2, 4, 5]
print((most_occuring_element(my_list)))
