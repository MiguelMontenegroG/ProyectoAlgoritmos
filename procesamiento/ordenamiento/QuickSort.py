def quicksort_inplace(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quicksort_inplace(arr, low, p - 1)
        quicksort_inplace(arr, p + 1, high)

def partition(arr, low, high):
    pivot = arr[high]  # Elegimos el último elemento como pivote
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Intercambiar
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
