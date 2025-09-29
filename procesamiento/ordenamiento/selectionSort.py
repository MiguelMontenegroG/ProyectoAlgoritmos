def selection_sort(arr):
    """
    Ordena una lista usando el algoritmo Selection Sort
    """
    n = len(arr)
    for i in range(n - 1):
        # Suponemos que el mínimo está en la posición i
        min_idx = i
        # Buscar el mínimo en el resto del arreglo
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Intercambiar si encontramos un valor menor
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
