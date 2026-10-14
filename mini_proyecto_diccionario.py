"""
Mini-Proyecto: Diccionario Inteligente (BST de objetos Palabra)
"""

import random
import unicodedata
from functools import total_ordering

def normalizar(texto):
    """Minusculas y sin tildes (conserva la ñ como letra distinta de la n)."""
    texto = texto.strip().lower().replace("ñ", "\x00")   # proteger la ñ
    descompuesto = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")
    return sin_tildes.replace("\x00", "ñ")

@total_ordering
class Palabra:

    def __init__(self, texto, definicion):
        self.texto = texto.strip()
        self.definicion = definicion.strip()
        self.clave = normalizar(self.texto)

    def __eq__(self, otra):
        return self.clave == otra.clave

    def __lt__(self, otra):
        return self.clave < otra.clave

    def __hash__(self):
        return hash(self.clave)

    def __str__(self):
        return f"{self.texto}: {self.definicion}"

    def __repr__(self):
        return f"Palabra({self.texto!r})"


class NodoPalabra:
    def __init__(self, palabra):
        self.palabra = palabra
        self.izquierdo = None
        self.derecho = None


class DiccionarioBST:
    """Arbol Binario de Busqueda cuyos nodos almacenan objetos Palabra."""

    def __init__(self):
        self.raiz = None
        self._total = 0

    def __len__(self):
        return self._total

    # ---------------- Insercion ----------------
    def insertar(self, palabra):
        """Inserta una Palabra. Retorna True si es nueva, False si ya existia
        (en ese caso se actualiza su definicion)."""
        if self.raiz is None:
            self.raiz = NodoPalabra(palabra)
            self._total += 1
            return True
        return self._insertar_rec(self.raiz, palabra)

    def _insertar_rec(self, nodo, palabra):
        if palabra < nodo.palabra:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoPalabra(palabra)
                self._total += 1
                return True
            return self._insertar_rec(nodo.izquierdo, palabra)
        if palabra > nodo.palabra:
            if nodo.derecho is None:
                nodo.derecho = NodoPalabra(palabra)
                self._total += 1
                return True
            return self._insertar_rec(nodo.derecho, palabra)
        # Misma clave: ya existe -> actualizar definicion
        nodo.palabra.definicion = palabra.definicion
        return False

    def agregar(self, texto, definicion):
        """ crea la Palabra y la inserta."""
        return self.insertar(Palabra(texto, definicion))

    # ---------------- Busqueda exacta ----------------
    def buscar(self, texto):
        """Retorna el objeto Palabra o None si no existe."""
        clave = normalizar(texto)
        nodo = self.raiz
        while nodo is not None:
            if clave == nodo.palabra.clave:
                return nodo.palabra
            nodo = nodo.izquierdo if clave < nodo.palabra.clave else nodo.derecho
        return None

    # ---------------- Busqueda por prefijo ----------------
    def buscar_por_prefijo(self, prefijo):
        """Retorna la lista (ordenada A-Z) de Palabras que empiezan con `prefijo`."""
        prefijo = normalizar(prefijo)
        resultado = []
        if prefijo:
            self._prefijo_rec(self.raiz, prefijo, resultado)
        return resultado

    def _prefijo_rec(self, nodo, prefijo, resultado):
        # Caso base: rama vacia
        if nodo is None:
            return
        inicio_clave = nodo.palabra.clave[:len(prefijo)]

        if prefijo < inicio_clave:
            # Todas las coincidencias son alfabeticamente menores -> solo izquierda
            self._prefijo_rec(nodo.izquierdo, prefijo, resultado)
        elif prefijo > inicio_clave:
            # Todas las coincidencias son mayores -> solo derecha
            self._prefijo_rec(nodo.derecho, prefijo, resultado)
        else:
            # Este nodo coincide; puede haber mas a ambos lados (orden inorden)
            self._prefijo_rec(nodo.izquierdo, prefijo, resultado)
            resultado.append(nodo.palabra)
            self._prefijo_rec(nodo.derecho, prefijo, resultado)

    # ---------------- Recorrido y utilidades ----------------
    def inorden(self):
        """Todas las palabras en orden alfabetico."""
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo is not None:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.palabra)
            self._inorden_rec(nodo.derecho, resultado)

    def altura(self):
        return self._altura_rec(self.raiz)

    def _altura_rec(self, nodo):
        if nodo is None:
            return -1
        return 1 + max(self._altura_rec(nodo.izquierdo), self._altura_rec(nodo.derecho))

    # ---------------- Carga desde archivo ----------------
    def cargar_desde_archivo(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            lineas = [l.strip() for l in archivo if l.strip() and not l.startswith("#")]
        random.shuffle(lineas)
        nuevas = 0
        for linea in lineas:
            if "|" not in linea:
                continue
            texto, definicion = linea.split("|", 1)
            if texto.strip() and self.agregar(texto, definicion):
                nuevas += 1
        return nuevas


# --------------------------------------------------------------------------
# Datos iniciales (58 palabras,sin orden alfabetico)
# --------------------------------------------------------------------------
PALABRAS_INICIALES = [
    ("mesa", "Mueble con una superficie plana sostenida por patas."),
    ("auto", "Vehículo de cuatro ruedas que se mueve por un motor."),
    ("zapato", "Calzado que cubre el pie."),
    ("autonomía", "Capacidad de actuar o decidir por uno mismo."),
    ("libro", "Conjunto de hojas impresas y encuadernadas."),
    ("aurora", "Luz rosada que aparece en el cielo antes de salir el sol."),
    ("casa", "Edificio donde vive una persona o una familia."),
    ("sol", "Estrella alrededor de la cual gira la Tierra."),
    ("autor", "Persona que crea una obra científica, literaria o artística."),
    ("perro", "Mamífero doméstico, fiel compañero del ser humano."),
    ("nube", "Masa de vapor de agua suspendida en la atmósfera."),
    ("árbol", "Planta de tronco leñoso que se ramifica a cierta altura del suelo."),
    ("teclado", "Conjunto de teclas de una computadora."),
    ("avión", "Aeronave con alas que vuela impulsada por motores."),
    ("río", "Corriente continua de agua que desemboca en el mar o en un lago."),
    ("automóvil", "Vehículo autopropulsado para el transporte de personas."),
    ("gato", "Mamífero felino doméstico de pelaje suave."),
    ("luna", "Satélite natural de la Tierra."),
    ("ventana", "Abertura en una pared para dar luz y ventilación."),
    ("autobús", "Vehículo de gran capacidad para el transporte público de pasajeros."),
    ("montaña", "Gran elevación natural del terreno."),
    ("reloj", "Instrumento que sirve para medir el tiempo."),
    ("bosque", "Terreno extenso poblado de árboles y plantas."),
    ("computadora", "Máquina electrónica que procesa información."),
    ("flor", "Parte de la planta donde se encuentran los órganos reproductores."),
    ("mar", "Gran masa de agua salada que cubre gran parte de la Tierra."),
    ("puente", "Construcción que permite cruzar un río, valle o carretera."),
    ("aula", "Sala donde se imparten las clases en un centro de enseñanza."),
    ("estrella", "Cuerpo celeste que brilla con luz propia."),
    ("camino", "Vía de tierra o sendero por donde se transita."),
    ("pan", "Alimento hecho con harina, agua y levadura cocido al horno."),
    ("lápiz", "Instrumento de escritura con una barra de grafito."),
    ("ciudad", "Población grande con muchos habitantes y servicios."),
    ("silla", "Asiento con respaldo y generalmente cuatro patas."),
    ("algoritmo", "Conjunto ordenado de pasos para resolver un problema."),
    ("pantalla", "Superficie donde se muestran imágenes o datos."),
    ("autógrafo", "Firma de una persona famosa escrita de su propia mano."),
    ("hoja", "Órgano laminar y verde de las plantas; también, lámina de papel."),
    ("raíz", "Parte de la planta que crece bajo tierra y absorbe agua y nutrientes."),
    ("escuela", "Establecimiento donde se da enseñanza a los estudiantes."),
    ("datos", "Información organizada que puede ser procesada."),
    ("puerta", "Abertura por la que se entra y se sale, con una hoja que la cierra."),
    ("nodo", "Elemento de una estructura de datos que guarda un valor y enlaces."),
    ("lluvia", "Agua que cae de las nubes en forma de gotas."),
    ("viento", "Corriente de aire que se desplaza en la atmósfera."),
    ("rama", "Cada una de las partes que nacen del tronco de un árbol."),
    ("tren", "Vehículo formado por vagones que circula sobre rieles."),
    ("autoridad", "Poder o facultad para mandar o hacerse obedecer."),
    ("fuego", "Calor y luz producidos por la combustión de un material."),
    ("tierra", "Planeta en que vivimos; también, el suelo natural."),
    ("isla", "Porción de tierra rodeada de agua por todas partes."),
    ("ñandú", "Ave corredora de gran tamaño, propia de Sudamérica."),
    ("jardín", "Terreno donde se cultivan plantas y flores de adorno."),
    ("cuaderno", "Conjunto de hojas cosidas o encuadernadas para escribir."),
    ("hormiga", "Insecto pequeño que vive en colonias muy organizadas."),
    ("programa", "Conjunto de instrucciones que ejecuta una computadora."),
    ("bicicleta", "Vehículo de dos ruedas que se mueve con pedales."),
    ("queso", "Alimento sólido que se obtiene de la leche cuajada."),
]


# --------------------------------------------------------------------------
# Interfaz de consola
# --------------------------------------------------------------------------
MENU = """
==============================================
         DICCIONARIO INTELIGENTE
==============================================
  1. Buscar una palabra (definición exacta)
  2. Autocompletar (buscar por prefijo)
  3. Ver el diccionario completo (A-Z)
  4. Agregar o actualizar una palabra
  5. Cargar palabras desde un archivo (.txt)
  6. Información del árbol
  0. Salir
----------------------------------------------"""


def cargar_diccionario_inicial():
    diccionario = DiccionarioBST()
    for texto, definicion in PALABRAS_INICIALES:
        diccionario.agregar(texto, definicion)
    return diccionario


def opcion_buscar(diccionario):
    texto = input("Palabra a buscar: ").strip()
    if not texto:
        print("  Debes escribir una palabra.")
        return
    palabra = diccionario.buscar(texto)
    if palabra:
        print(f"\n  {palabra.texto.upper()}\n  {palabra.definicion}")
    else:
        print(f"\n  '{texto}' no esta en el diccionario.")
        sugerencias = diccionario.buscar_por_prefijo(texto[:2]) if len(texto) >= 2 else []
        if sugerencias:
            nombres = ", ".join(p.texto for p in sugerencias[:5])
            print(f"  ¿Quisiste decir alguna de estas? {nombres}")


def opcion_prefijo(diccionario):
    prefijo = input("Escribe el prefijo (ej: au): ").strip()
    if not prefijo:
        print("  Debes escribir un prefijo.")
        return
    coincidencias = diccionario.buscar_por_prefijo(prefijo)
    if not coincidencias:
        print(f"\n  No hay palabras que empiecen con '{prefijo}'.")
        return
    print(f"\n  {len(coincidencias)} coincidencia(s) para '{prefijo}':")
    for palabra in coincidencias:
        print(f"   - {palabra.texto}")


def opcion_listar(diccionario):
    palabras = diccionario.inorden()
    print(f"\n  Diccionario completo ({len(palabras)} palabras):\n")
    for palabra in palabras:
        print(f"  {palabra.texto:<14} {palabra.definicion}")


def opcion_agregar(diccionario):
    texto = input("Nueva palabra: ").strip()
    definicion = input("Definicion: ").strip()
    if not texto or not definicion:
        print("  La palabra y la definicion no pueden estar vacias.")
        return
    if diccionario.agregar(texto, definicion):
        print(f"  '{texto}' agregada.")
    else:
        print(f"  '{texto}' ya existia: se actualizo su definicion.")


def opcion_cargar_archivo(diccionario):
    ruta = input("Ruta del archivo (formato palabra|definicion por linea): ").strip()
    try:
        nuevas = diccionario.cargar_desde_archivo(ruta)
        print(f"  Se agregaron {nuevas} palabras nuevas.")
    except OSError as error:
        print(f"  No se pudo leer el archivo: {error}")


def opcion_info(diccionario):
    print(f"\n  Palabras almacenadas : {len(diccionario)}")
    print(f"  Altura del arbol     : {diccionario.altura()}")


def main():
    diccionario = cargar_diccionario_inicial()
    print(f"Diccionario cargado con {len(diccionario)} palabras.")

    acciones = {
        "1": opcion_buscar,
        "2": opcion_prefijo,
        "3": opcion_listar,
        "4": opcion_agregar,
        "5": opcion_cargar_archivo,
        "6": opcion_info,
    }

    while True:
        print(MENU)
        try:
            opcion = input("Elige una opcion: ").strip()
            if opcion == "0":
                break
            accion = acciones.get(opcion)
            if accion:
                accion(diccionario)
            else:
                print("  Opcion no valida, intenta de nuevo.")
        except (EOFError, KeyboardInterrupt):
            print()
            break
    print("\n¡Hasta pronto!")


if __name__ == "__main__":
    main()
