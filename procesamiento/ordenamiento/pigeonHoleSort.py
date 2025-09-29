def pigeonhole_sort(arr):
    """
    Ordena una lista de números enteros usando Pigeonhole Sort.
    :param arr: Lista de enteros a ordenar.
    :return: Lista ordenada.
    """
    if not arr:   # Si la lista está vacía, no hace nada
        return arr

    # 1️⃣ Encontrar el valor mínimo y máximo
    min_val = min(arr)
    max_val = max(arr)

    # 2️⃣ Calcular el rango
    size = max_val - min_val + 1

    # 3️⃣ Crear las "pigeonholes" (casillas)
    holes = [0] * size

    # 4️⃣ Contar las ocurrencias de cada número
    for num in arr:
        holes[num - min_val] += 1

    # 5️⃣ Reconstruir el arreglo ordenado
    i = 0
    for index in range(size):
        while holes[index] > 0:
            arr[i] = index + min_val
            i += 1
            holes[index] -= 1

    return arr