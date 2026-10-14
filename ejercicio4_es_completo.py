"""
Ejercicio 4 - es_completo()
"""

from arbol_bst import ArbolBinarioBusqueda


class ArbolConEsCompleto(ArbolBinarioBusqueda):

    def es_completo(self):
        return self._es_completo_recursivo(self.raiz)

    def _es_completo_recursivo(self, nodo):
        # Caso base 1: subarbol vacio, no incumple nada
        if nodo is None:
            return True
        # Caso base 2: hoja, no es nodo interno
        if nodo.izquierdo is None and nodo.derecho is None:
            return True
        # Caso base 3: nodo con UN solo hijo -> incumple la condicion
        if nodo.izquierdo is None or nodo.derecho is None:
            return False
        # Caso recursivo: tiene dos hijos, ambos subarboles deben cumplir
        return (self._es_completo_recursivo(nodo.izquierdo)
                and self._es_completo_recursivo(nodo.derecho))


if __name__ == "__main__":
    def crear(valores):
        arbol = ArbolConEsCompleto()
        for v in valores:
            arbol.insertar(v)
        return arbol

    casos = [
        ("Vacio", []),
        ("Solo raiz", [10]),
        ("Perfecto (7 nodos)", [50, 30, 70, 20, 40, 60, 80]),
        ("Lleno pero no perfecto", [50, 30, 70, 20, 40]),
        ("Un nodo con un solo hijo", [50, 30, 70, 20]),
        ("Degenerado", [1, 2, 3, 4, 5]),
    ]
    for nombre, valores in casos:
        print(f"{nombre:28} {valores!s:28} -> {crear(valores).es_completo()}")
