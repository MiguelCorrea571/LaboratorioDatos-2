import csv

class NodoAVL:
    def __init__(self, med, nombre, iso3, temperaturas, padre=None):
        self.med = med
        self.nombre = nombre
        self.iso3 = iso3
        self.temperaturas = temperaturas
        self.izq = None
        self.der = None
        self.padre = padre
        self.altura = 1


class ArbolAVL:
    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izq) - self.obtener_altura(nodo.der)

    # ---------------- ROTACIONES ----------------
    def rotar_derecha(self, y):
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        if T2: T2.padre = y
        x.padre = y.padre
        y.padre = x
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        x.altura = 1 + max(self.obtener_altura(x.izq), self.obtener_altura(x.der))
        return x

    def rotar_izquierda(self, x):
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        if T2: T2.padre = x
        y.padre = x.padre
        x.padre = y
        x.altura = 1 + max(self.obtener_altura(x.izq), self.obtener_altura(x.der))
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        return y

    # ---------------- INSERTAR ----------------
    def insertar(self, raiz, med, nombre, iso3, temperaturas, padre=None):
        if not raiz:
            return NodoAVL(med, nombre, iso3, temperaturas, padre)
        elif med < raiz.med:
            raiz.izq = self.insertar(raiz.izq, med, nombre, iso3, temperaturas, raiz)
        elif med > raiz.med:
            raiz.der = self.insertar(raiz.der, med, nombre, iso3, temperaturas, raiz)
        else:
            return raiz

        raiz.altura = 1 + max(self.obtener_altura(raiz.izq), self.obtener_altura(raiz.der))
        balance = self.obtener_balance(raiz)

        # Rotaciones AVL
        if balance > 1 and med < raiz.izq.med:
            return self.rotar_derecha(raiz)
        if balance < -1 and med > raiz.der.med:
            return self.rotar_izquierda(raiz)
        if balance > 1 and med > raiz.izq.med:
            raiz.izq = self.rotar_izquierda(raiz.izq)
            return self.rotar_derecha(raiz)
        if balance < -1 and med < raiz.der.med:
            raiz.der = self.rotar_derecha(raiz.der)
            return self.rotar_izquierda(raiz)

        return raiz

    # ---------------- ELIMINAR ----------------
    def eliminar(self, raiz, med):
        if not raiz:
            return raiz
        if med < raiz.med:
            raiz.izq = self.eliminar(raiz.izq, med)
        elif med > raiz.med:
            raiz.der = self.eliminar(raiz.der, med)
        else:
            if not raiz.izq:
                temp = raiz.der
                if temp: temp.padre = raiz.padre
                return temp
            elif not raiz.der:
                temp = raiz.izq
                if temp: temp.padre = raiz.padre
                return temp
            temp = self.minimo(raiz.der)
            raiz.med = temp.med
            raiz.nombre = temp.nombre
            raiz.iso3 = temp.iso3
            raiz.temperaturas = temp.temperaturas
            raiz.der = self.eliminar(raiz.der, temp.med)

        raiz.altura = 1 + max(self.obtener_altura(raiz.izq), self.obtener_altura(raiz.der))
        balance = self.obtener_balance(raiz)

        if balance > 1 and self.obtener_balance(raiz.izq) >= 0:
            return self.rotar_derecha(raiz)
        if balance > 1 and self.obtener_balance(raiz.izq) < 0:
            raiz.izq = self.rotar_izquierda(raiz.izq)
            return self.rotar_derecha(raiz)
        if balance < -1 and self.obtener_balance(raiz.der) <= 0:
            return self.rotar_izquierda(raiz)
        if balance < -1 and self.obtener_balance(raiz.der) > 0:
            raiz.der = self.rotar_derecha(raiz.der)
            return self.rotar_izquierda(raiz)

        return raiz

    def minimo(self, nodo):
        current = nodo
        while current.izq:
            current = current.izq
        return current

    # ---------------- BÚSQUEDAS ----------------
    def buscar_por_media(self, nodo, med):
        if nodo is None:
            return None
        if nodo.med == med:
            return nodo
        elif med < nodo.med:
            return self.buscar_por_media(nodo.izq, med)
        else:
            return self.buscar_por_media(nodo.der, med)

    def buscar_temperatura_anio_mayor_promedio(self, nodo, anio, promedio_anio, resultado):
        if nodo:
            self.buscar_temperatura_anio_mayor_promedio(nodo.izq, anio, promedio_anio, resultado)
            if nodo.temperaturas[f"F{anio}"] > promedio_anio:
                resultado.append(nodo)
            self.buscar_temperatura_anio_mayor_promedio(nodo.der, anio, promedio_anio, resultado)

    def buscar_temperatura_anio_menor_promedio_global(self, nodo, promedio_global, resultado):
        if nodo:
            self.buscar_temperatura_anio_menor_promedio_global(nodo.izq, promedio_global, resultado)
            for temp in nodo.temperaturas.values():
                if temp < promedio_global:
                    resultado.append(nodo)
                    break
            self.buscar_temperatura_anio_menor_promedio_global(nodo.der, promedio_global, resultado)

    def buscar_media_mayor_o_igual(self, nodo, valor, resultado):
        if nodo:
            self.buscar_media_mayor_o_igual(nodo.izq, valor, resultado)
            if nodo.med >= valor:
                resultado.append(nodo)
            self.buscar_media_mayor_o_igual(nodo.der, valor, resultado)

    # ---------------- MOSTRAR ----------------
    def mostrar_arbol(self, nodo, nivel=0):
        if nodo:
            self.mostrar_arbol(nodo.der, nivel + 1)
            print("    " * nivel + f"{nodo.nombre} ({nodo.med:.2f})")
            self.mostrar_arbol(nodo.izq, nivel + 1)

    # ---------------- RECORRIDO POR NIVELES ----------------
    def altura_arbol(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self.altura_arbol(nodo.izq), self.altura_arbol(nodo.der))

    def imprimir_nivel(self, nodo, nivel):
        if nodo is None:
            return
        if nivel == 1:
            print(nodo.iso3, end=" ")
        else:
            self.imprimir_nivel(nodo.izq, nivel - 1)
            self.imprimir_nivel(nodo.der, nivel - 1)

    def recorrido_por_niveles(self, raiz):
        h = self.altura_arbol(raiz)
        for i in range(1, h + 1):
            self.imprimir_nivel(raiz, i)
            print()

    # ---------------- NODO SELECCIONADO ----------------
    def nivel_nodo(self, nodo):
        nivel = 0
        while nodo.padre:
            nodo = nodo.padre
            nivel += 1
        return nivel

    def padre(self, nodo):
        return nodo.padre

    def abuelo(self, nodo):
        if nodo.padre:
            return nodo.padre.padre
        return None

    def tio(self, nodo):
        abu = self.abuelo(nodo)
        if not abu:
            return None
        if abu.izq == nodo.padre:
            return abu.der
        else:
            return abu.izq


# ---------------- BLOQUE PRINCIPAL ----------------
if __name__ == "__main__":
    avl = ArbolAVL()
    raiz = None
    all_temps_por_anio = {f"F{anio}": [] for anio in range(1961, 2023)}
    all_temps_global = []

    with open("dataset_climate_change.csv", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            temps = [float(fila[f"F{anio}"]) for anio in range(1961, 2023)]
            for i, t in enumerate(temps):
                all_temps_por_anio[f"F{1961 + i}"].append(t)
                all_temps_global.append(t)
            med = sum(temps) / len(temps)
            nombre = fila["Country"]
            iso3 = fila["ISO3"]
            temperaturas = {f"F{1961 + i}": temps[i] for i in range(len(temps))}
            raiz = avl.insertar(raiz, med, nombre, iso3, temperaturas)

    # ---------------- PROMEDIOS ----------------
    promedio_global = sum(all_temps_global) / len(all_temps_global)

    anio = 2000
    promedio_anio = sum(all_temps_por_anio[f"F{anio}"]) / len(all_temps_por_anio[f"F{anio}"])

    # ---------------- BÚSQUEDAS ----------------
    resultado_a = []
    avl.buscar_temperatura_anio_mayor_promedio(raiz, anio, promedio_anio, resultado_a)

    resultado_b = []
    avl.buscar_temperatura_anio_menor_promedio_global(raiz, promedio_global, resultado_b)

    valor_c = 0.10
    resultado_c = []
    avl.buscar_media_mayor_o_igual(raiz, valor_c, resultado_c)

    # ---------------- MOSTRAR ----------------
    print("\nÁrbol AVL visualizado (nombre y media):")
    avl.mostrar_arbol(raiz)

    print("\nRecorrido por niveles (solo ISO3):")
    avl.recorrido_por_niveles(raiz)

    # ---------------- EJEMPLO NODOS SELECCIONADOS ----------------
    if resultado_a:
        nodo_a = resultado_a[0]
        print("\n===== Nodo criterio A: Temperatura mayor al promedio en un año =====")
        print(f"País: {nodo_a.nombre}")
        print("  Nivel:", avl.nivel_nodo(nodo_a))
        print("  Factor de balance:", avl.obtener_balance(nodo_a))
        print("  Padre:", avl.padre(nodo_a).nombre if avl.padre(nodo_a) else None)
        print("  Abuelo:", avl.abuelo(nodo_a).nombre if avl.abuelo(nodo_a) else None)
        tio = avl.tio(nodo_a)
        print("  Tío:", tio.nombre if tio else None)

    if resultado_b:
        nodo_b = resultado_b[0]
        print("\n===== Nodo criterio B: Temperatura menor al promedio global =====")
        print(f"País: {nodo_b.nombre}")
        print("  Nivel:", avl.nivel_nodo(nodo_b))
        print("  Factor de balance:", avl.obtener_balance(nodo_b))
        print("  Padre:", avl.padre(nodo_b).nombre if avl.padre(nodo_b) else None)
        print("  Abuelo:", avl.abuelo(nodo_b).nombre if avl.abuelo(nodo_b) else None)
        tio = avl.tio(nodo_b)
        print("  Tío:", tio.nombre if tio else None)

    if resultado_c:
        nodo_c = resultado_c[0]
        print("\n===== Nodo criterio C: Temperatura media >= valor dado =====")
        print(f"País: {nodo_c.nombre}")
        print("  Nivel:", avl.nivel_nodo(nodo_c))
        print("  Factor de balance:", avl.obtener_balance(nodo_c))
        print("  Padre:", avl.padre(nodo_c).nombre if avl.padre(nodo_c) else None)
        print("  Abuelo:", avl.abuelo(nodo_c).nombre if avl.abuelo(nodo_c) else None)
        tio = avl.tio(nodo_c)
        print("  Tío:", tio.nombre if tio else None)
