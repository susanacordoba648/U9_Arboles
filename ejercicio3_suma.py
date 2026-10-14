"""
Ejercicio 3 - Suma de todos los elementos de un BST sin modificarlo.
"""

from arbol_bst import ArbolBinarioBusqueda


def suma_arbol(arbol):
    """Retorna la suma de todos los valores del BST (0 si esta vacio)."""
    return _suma_recursiva(arbol.raiz)


def _suma_recursiva(nodo):
    # Caso base: un subarbol vacio suma 0
    if nodo is None:
        return 0
    # Caso recursivo: este nodo + lo que sumen sus dos subarboles
    return nodo.valor + _suma_recursiva(nodo.izquierdo) + _suma_recursiva(nodo.derecho)


if __name__ == "__main__":
    arbol = ArbolBinarioBusqueda()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        arbol.insertar(v)

    antes = arbol.preorden()
    print("Arbol (inorden):", arbol.inorden())
    print("Suma:", suma_arbol(arbol))      # 50+30+70+20+40+60+80 = 350
    despues = arbol.preorden()

    assert suma_arbol(arbol) == sum(arbol.inorden())
    assert antes == despues, "¡El árbol fue modificado!"
    print("OK: el arbol original no fue modificado.")

    print("Suma de arbol vacio:", suma_arbol(ArbolBinarioBusqueda()))   # 0
