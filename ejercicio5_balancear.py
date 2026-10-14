"""
Ejercicio 5 - balancear_arbol()
"""

import math

from arbol_bst import ArbolBinarioBusqueda, NodoArbol


def balancear_arbol(arbol):
    """Retorna un NUEVO ArbolBinarioBusqueda balanceado con los mismos valores."""
    valores = arbol.inorden()              # ordenados de menor a mayor
    nuevo = ArbolBinarioBusqueda()
    nuevo.raiz = _construir_balanceado(valores, 0, len(valores) - 1)
    return nuevo


def _construir_balanceado(valores, inicio, fin):
    # Caso base: rango vacio -> no hay nodo
    if inicio > fin:
        return None
    # Caso recursivo: el elemento central sera la raiz de este subarbol
    medio = (inicio + fin) // 2
    nodo = NodoArbol(valores[medio])
    nodo.izquierdo = _construir_balanceado(valores, inicio, medio - 1)
    nodo.derecho = _construir_balanceado(valores, medio + 1, fin)
    return nodo


def altura(nodo):
    """Altura en aristas (arbol vacio = -1), igual que en la practica de clase."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


if __name__ == "__main__":
    # Arbol degenerado: insertar en orden creciente lo convierte en una lista
    degenerado = ArbolBinarioBusqueda()
    for v in range(1, 16):
        degenerado.insertar(v)

    balanceado = balancear_arbol(degenerado)

    print("Altura original  :", altura(degenerado.raiz))    # 14
    print("Altura balanceado:", altura(balanceado.raiz))     # 3
    print("Inorden original :", degenerado.inorden())
    print("Inorden nuevo    :", balanceado.inorden())
    print("Preorden nuevo   :", balanceado.preorden())
    print()
    balanceado.mostrar_arbol()

    # Verificaciones automaticas con distintos tamaños
    for n in [0, 1, 2, 5, 10, 100]:
        t = ArbolBinarioBusqueda()
        for v in range(n):
            t.insertar(v)
        b = balancear_arbol(t)
        assert b.inorden() == list(range(n))
        if n > 0:
            assert altura(b.raiz) == int(math.log2(n)), f"n={n}"
    print("\nOK: misma informacion y altura minima floor(log2 n) en todas las pruebas.")
