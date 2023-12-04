def weighted_levenshtein(str1, str2, weight_dict):
    """
    Calcula la distancia de Levenshtein considerando las posiciones dinámicas de los caracteres después de cada operación,
    donde las posiciones se recalculan dinámicamente después de cada inserción, eliminación o sustitución.

    :param str1: Primera cadena.
    :param str2: Segunda cadena.
    :param weight_dict: Diccionario con pesos para cada operación y carácter según su posición.
    :return: Distancia de Levenshtein y lista de operaciones realizadas.


    Calculates the Levenshtein distance considering the dynamic positions of the characters after each operation,
    where positions are dynamically recalculated after each insertion, deletion or replacement.

    :param str1: First string.
    :param str2: Second string.
    :param weight_dict: Dictionary with weights for each operation and character according to its position.
    :return: Levenshtein distance and list of operations performed.
    """
    len_str1 = len(str1)
    len_str2 = len(str2)

    # Inicializa la matriz de distancia y la matriz de operaciones
    # Initialize the distance matrix and operation matrix
    dist_matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]
    #op_matrix = [[[] for _ in range(len_str2 + 1)] for _ in range(len_str1 + 1)]

    # Inicializa la primera fila y columna   
    # Initialize the first row and column
    for i in range(1, len_str1 + 1):
        dist_matrix[i][0] = dist_matrix[i - 1][0] + weight_dict.get(('delete', str1[i - 1], 'start' if i == 1 else 'middle'), 1)
        #op_matrix[i][0] = op_matrix[i - 1][0] + [('delete', str1[i - 1], 'start' if i == 1 else 'middle')]
    for j in range(1, len_str2 + 1):
        dist_matrix[0][j] = dist_matrix[0][j - 1] + weight_dict.get(('insert', str2[j - 1], 'start' if j == 1 else 'middle'), 1)
        #op_matrix[0][j] = op_matrix[0][j - 1] + [('insert', str2[j - 1], 'start' if j == 1 else 'middle')]

    # Función para determinar la posición actual de un carácter en una palabra
    # Function to determine the current position of a character in a word
    def current_position(i, j, original_i, original_j):
        if i == 1 and j == 1:
            return 'start'
        elif i == original_i and j == original_j:
            return 'end'
        else:
            return 'middle'

    # Rellena la matriz de distancia y la matriz de operaciones
    # Fill the distance matrix and the operations matrix
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            pos1 = current_position(i, j, len_str1, len_str2) 
            pos2 = current_position(i, j, len_str1, len_str2)

            # Calcula los costos para las operaciones de inserción, eliminación y sustitución
            # Calculates costs for insert, delete, and replace operations
            insertion_cost = dist_matrix[i][j - 1] + weight_dict.get(('insert', str2[j - 1], pos2), 0.96)
            deletion_cost = dist_matrix[i - 1][j] + weight_dict.get(('delete', str1[i - 1], pos1), 0.96)
            substitution_cost = dist_matrix[i - 1][j - 1]
            if str1[i - 1] != str2[j - 1]:
                substitution_cost += weight_dict.get(('substitute', str1[i - 1], str2[j - 1], pos1), 1)

            # Determina la operación mínima y actualiza la matriz de operaciones
            # Determine the minimum operation and update the operation matrix
            if insertion_cost < deletion_cost and insertion_cost < substitution_cost:
                dist_matrix[i][j] = insertion_cost
                #op_matrix[i][j] = op_matrix[i][j - 1] + [('insert', str2[j - 1], pos2)]
            elif deletion_cost < substitution_cost:
                dist_matrix[i][j] = deletion_cost
                #op_matrix[i][j] = op_matrix[i - 1][j] + [('delete', str1[i - 1], pos1)]
            else:
                dist_matrix[i][j] = substitution_cost
                #print(str1[i - 1], str2[j - 1])
                #if str1[i - 1] != str2[j - 1]:
                    #op_matrix[i][j] = op_matrix[i - 1][j - 1] + [('substitute', str1[i - 1], str2[j - 1], pos1)]
                #else:
                    #op_matrix[i][j] = op_matrix[i - 1][j - 1]

    return dist_matrix[len_str1][len_str2]
#, op_matrix[len_str1][len_str2]