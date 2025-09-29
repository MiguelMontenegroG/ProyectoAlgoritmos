def gnome_sort(arr):
    """
    Ordena una lista usando el algoritmo Gnome Sort.
    - arr: lista de números o strings comparables
    Retorna: la misma lista ordenada (in-place)
    """
    index = 0
    n = len(arr)

    while index < n:
        # Si estamos al principio o el elemento actual está en orden con el anterior
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            # Intercambiar elementos desordenados
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr
