def heapify(arr, n, i):
    """
    Mantiene la propiedad de un heap máximo.
    arr: lista de elementos
    n: tamaño del heap
    i: índice actual
    """
    largest = i           # Inicialmente asumimos que el nodo raíz es el más grande
    left = 2 * i + 1      # Hijo izquierdo
    right = 2 * i + 2     # Hijo derecho

    # Si el hijo izquierdo es mayor que la raíz
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Si el hijo derecho es mayor que el más grande hasta ahora
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Si el más grande no es la raíz
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Intercambiar
        heapify(arr, n, largest)  # Llamar recursivamente para asegurar el heap


def heap_sort(arr):
    n = len(arr)

    # Construir un heap máximo
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extraer elementos uno por uno
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Mover el actual máximo al final
        heapify(arr, i, 0)  # Aplicar heapify a la raíz para reducir el heap

    return arr
