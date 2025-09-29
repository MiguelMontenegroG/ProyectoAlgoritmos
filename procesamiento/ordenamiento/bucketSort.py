def bucket_sort(arr):
    if len(arr) == 0:
        return arr  # Si está vacío, no hay nada que ordenar

    # 1️⃣ Encontrar el valor máximo y mínimo
    min_val, max_val = min(arr), max(arr)

    # 2️⃣ Elegir el número de buckets
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    # 3️⃣ Distribuir los elementos en los buckets
    for num in arr:
        # Calcular índice del bucket
        index = int((num - min_val) / (max_val - min_val + 1) * bucket_count)
        buckets[index].append(num)

    # 4️⃣ Ordenar cada bucket individualmente (usamos sorted())
    for i in range(bucket_count):
        buckets[i] = sorted(buckets[i])

    # 5️⃣ Combinar todos los buckets
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr
