"""
Ejercicio 1 - Eliminar un valor de un Arbol Binario de Busqueda.
"""

from arbol_bst import ArbolBinarioBusqueda


class ArbolConEliminar(ArbolBinarioBusqueda):

    def eliminar(self, valor):
        """Elimina `valor` del arbol. Retorna True si existia, False si no."""
        self.raiz, eliminado = self._eliminar_recursivo(self.raiz, valor)
        return eliminado

    def _eliminar_recursivo(self, nodo, valor):
        """Retorna (nueva_raiz_del_subarbol, fue_eliminado)."""
        # Caso base: llegamos a None, el valor no esta en el arbol
        if nodo is None:
            return None, False

        # Caso recursivo: seguir bajando segun la propiedad del BST
        if valor < nodo.valor:
            nodo.izquierdo, eliminado = self._eliminar_recursivo(nodo.izquierdo, valor)
            return nodo, eliminado
        if valor > nodo.valor:
            nodo.derecho, eliminado = self._eliminar_recursivo(nodo.derecho, valor)
            return nodo, eliminado

        # --- Aqui nodo.valor == valor: este es el nodo a eliminar ---

        # Caso 1: hoja
        if nodo.izquierdo is None and nodo.derecho is None:
            return None, True

        # Caso 2: un solo hijo -> el hijo ocupa el lugar del nodo
        if nodo.izquierdo is None:
            return nodo.derecho, True
        if nodo.derecho is None:
            return nodo.izquierdo, True

        # Caso 3: dos hijos -> sucesor inorden (mínimo del subarbol derecho)
        sucesor = self._nodo_minimo(nodo.derecho)
        nodo.valor = sucesor.valor
        nodo.derecho, _ = self._eliminar_recursivo(nodo.derecho, sucesor.valor)
        return nodo, True

    @staticmethod
    def _nodo_minimo(nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo


if __name__ == "__main__":
    def construir():
        arbol = ArbolConEliminar()
        for v in [50, 30, 70, 20, 40, 60, 80, 65]:
            arbol.insertar(v)
        return arbol

    arbol = construir()
    print("Arbol original:")
    arbol.mostrar_arbol()
    print("Inorden:", arbol.inorden())

    print("\n--- Caso 1: eliminar hoja (20) ---")
    print("Eliminado:", arbol.eliminar(20))
    print("Inorden:", arbol.inorden())

    print("\n--- Caso 2: eliminar nodo con 1 hijo (60, hijo derecho 65) ---")
    print("Eliminado:", arbol.eliminar(60))
    print("Inorden:", arbol.inorden())

    print("\n--- Caso 3: eliminar nodo con 2 hijos (30) ---")
    print("Eliminado:", arbol.eliminar(30))
    print("Inorden:", arbol.inorden())

    print("\n--- Caso 3 sobre la raíz (50) ---")
    print("Eliminado:", arbol.eliminar(50))
    print("Inorden:", arbol.inorden())
    arbol.mostrar_arbol()

    print("\n--- Valor inexistente (999) ---")
    print("Eliminado:", arbol.eliminar(999))

    # Verificacion automatica: el inorden debe seguir ordenado
    resultado = arbol.inorden()
    assert resultado == sorted(resultado), "¡El BST perdio su propiedad!"
    print("\nOK: el arbol sigue siendo un BST valido.")
