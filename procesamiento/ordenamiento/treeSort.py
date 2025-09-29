# treeSort.py

# Nodo del árbol
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

# Insertar respetando duplicados
def insertar(raiz, valor):
    if raiz is None:
        return Nodo(valor)
    if valor <= raiz.valor:  # Duplicados a la izquierda
        raiz.izquierda = insertar(raiz.izquierda, valor)
    else:
        raiz.derecha = insertar(raiz.derecha, valor)
    return raiz

# Recorrido inorden para obtener arreglo ordenado
def inorden(raiz, resultado):
    if raiz:
        inorden(raiz.izquierda, resultado)
        resultado.append(raiz.valor)
        inorden(raiz.derecha, resultado)

# Función principal TreeSort
def tree_sort(arreglo):
    raiz = None
    for valor in arreglo:
        raiz = insertar(raiz, valor)

    resultado = []
    inorden(raiz, resultado)

    # Reemplaza los valores originales en el arreglo
    for i in range(len(arreglo)):
        arreglo[i] = resultado[i]
