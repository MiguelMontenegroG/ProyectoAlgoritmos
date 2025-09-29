def binary_insertion_sort(arr):
    """
    Ordena una lista usando inserción binaria.
    - arr: lista de números o strings comparables
    Retorna: la misma lista ordenada (in-place)
    """
    for i in range(1, len(arr)):
        key = arr[i]

        # Buscar la posición donde insertar 'key' en arr[0..i-1]
        left, right = 0, i - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] > key:
                right = mid - 1
            else:
                left = mid + 1

        # Mover los elementos a la derecha para hacer espacio
        j = i - 1
        while j >= left:
            arr[j + 1] = arr[j]
            j -= 1

        # Insertar el elemento en la posición encontrada
        arr[left] = key

    return arr
