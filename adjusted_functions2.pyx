
# Cython language level directive
# cython: language_level=3

# Importing Cython types
from libc.stdint cimport int32_t
import numpy as np
cimport numpy as np

cpdef weighted_levenshtein(str str1, str str2, dict weight_dict):
    cdef:
        int len_str1 = len(str1), len_str2 = len(str2)
        int i, j
        double insertion_cost, deletion_cost, substitution_cost
        double[:, :] dist_matrix = np.zeros((len_str1 + 1, len_str2 + 1), dtype=np.double)

    # Initialize the first row and column of the distance matrix
    for i in range(1, len_str1 + 1):
        dist_matrix[i][0] = dist_matrix[i - 1][0] + weight_dict.get(('delete', str1[i - 1], 'start' if i == 1 else 'middle'), 1)
    for j in range(1, len_str2 + 1):
        dist_matrix[0][j] = dist_matrix[0][j - 1] + weight_dict.get(('insert', str2[j - 1], 'start' if j == 1 else 'middle'), 1)

    # Fill the distance matrix
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            # Determine positions
            pos1 = 'start' if i == 1 and j == 1 else ('end' if i == len_str1 and j == len_str2 else 'middle')
            pos2 = pos1

            # Calculate costs for insert, delete, and replace operations
            insertion_cost = dist_matrix[i][j - 1] + weight_dict.get(('insert', str2[j - 1], pos2), 0.96)
            deletion_cost = dist_matrix[i - 1][j] + weight_dict.get(('delete', str1[i - 1], pos1), 0.96)
            substitution_cost = dist_matrix[i - 1][j - 1]
            if str1[i - 1] != str2[j - 1]:
                substitution_cost += weight_dict.get(('substitute', str1[i - 1], str2[j - 1], pos1), 1)

            # Determine the minimum operation and update the matrix
            if insertion_cost < deletion_cost and insertion_cost < substitution_cost:
                dist_matrix[i][j] = insertion_cost
            elif deletion_cost < substitution_cost:
                dist_matrix[i][j] = deletion_cost
            else:
                dist_matrix[i][j] = substitution_cost
                #print(str1[i - 1], str2[j - 1])

    return dist_matrix[len_str1][len_str2]


