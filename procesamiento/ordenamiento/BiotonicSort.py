def bitonic_sort(arr, ascending=True):
    """
    Ordena una lista usando el algoritmo Bitonic Sort.
    :param arr: Lista de números a ordenar.
    :param ascending: True para ordenar ascendente, False para descendente.
    :return: Lista ordenada.
    """
    def compare_and_swap(arr, i, j, ascending):
        if (ascending and arr[i] > arr[j]) or (not ascending and arr[i] < arr[j]):
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(arr, low, cnt, ascending):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                compare_and_swap(arr, i, i + k, ascending)
            bitonic_merge(arr, low, k, ascending)
            bitonic_merge(arr, low + k, k, ascending)

    def bitonic_sort_rec(arr, low, cnt, ascending):
        if cnt > 1:
            k = cnt // 2
            # Crear secuencia bitónica
            bitonic_sort_rec(arr, low, k, True)
            bitonic_sort_rec(arr, low + k, k, False)
            bitonic_merge(arr, low, cnt, ascending)

    n = len(arr)
    bitonic_sort_rec(arr, 0, n, ascending)
    return arr
