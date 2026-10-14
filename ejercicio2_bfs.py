"""
Ejercicio 2 - Recorrido por niveles (BFS) usando una Cola.
"""

from collections import deque

from arbol_bst import ArbolBinarioBusqueda


class ArbolConBFS(ArbolBinarioBusqueda):

    def por_niveles(self):
        """Retorna una lista plana con los valores recorridos por niveles."""
        resultado = []
        if self.raiz is None:
            return resultado

        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()          # sacar el primero de la cola
            resultado.append(nodo.valor)   # visitarlo
            if nodo.izquierdo is not None:
                cola.append(nodo.izquierdo)
            if nodo.derecho is not None:
                cola.append(nodo.derecho)
        return resultado

    def por_niveles_agrupados(self):
        """Version extra: retorna una lista de listas, una por nivel."""
        niveles = []
        if self.raiz is None:
            return niveles

        cola = deque([self.raiz])
        while cola:
            cantidad_nivel = len(cola)     # nodos que hay en el nivel actual
            nivel = []
            for _ in range(cantidad_nivel):
                nodo = cola.popleft()
                nivel.append(nodo.valor)
                if nodo.izquierdo is not None:
                    cola.append(nodo.izquierdo)
                if nodo.derecho is not None:
                    cola.append(nodo.derecho)
            niveles.append(nivel)
        return niveles


if __name__ == "__main__":
    arbol = ArbolConBFS()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        arbol.insertar(v)

    arbol.mostrar_arbol()
    print("\nPor niveles (BFS):", arbol.por_niveles())
    # Esperado: [50, 30, 70, 20, 40, 60, 80]
    print("Agrupado por nivel:", arbol.por_niveles_agrupados())
    # Esperado: [[50], [30, 70], [20, 40, 60, 80]]

    print("Inorden (DFS) :", arbol.inorden())
    print("Preorden (DFS):", arbol.preorden())

    vacio = ArbolConBFS()
    print("Arbol vacio   :", vacio.por_niveles())
