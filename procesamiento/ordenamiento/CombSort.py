def comb_sort(arr):
    """
    Ordena una lista usando el algoritmo Comb Sort
    """
    n = len(arr)
    gap = n                # Gap inicial igual al tamaño del arreglo
    shrink = 1.3            # Factor de reducción típico
    swapped = True          # Para saber si hubo intercambios

    # Mientras el gap sea mayor que 1 o haya habido swaps
    while gap > 1 or swapped:
        # Reducir el gap en cada iteración
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1

        swapped = False

        # Comparar y cambiar elementos separados por el gap
        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
    return arr
