
#hacer y terminar
class MonticuloBinario:
    
    def __init__(self, es_min=True):
        self.listaMonticulo = [0]
        self.tamanoActual = 0
        self.es_min = es_min

    def infiltArriba(self, i):
        while i // 2 > 0:
            if (self.es_min and self.listaMonticulo[i] < self.listaMonticulo[i // 2]) or \
               (not self.es_min and self.listaMonticulo[i] > self.listaMonticulo[i // 2]):
                self.listaMonticulo[i], self.listaMonticulo[i // 2] = self.listaMonticulo[i // 2], self.listaMonticulo[i]
            i = i // 2

    def insertar(self, k):
        self.listaMonticulo.append(k)
        self.tamanoActual += 1
        self.infiltArriba(self.tamanoActual)

    def infiltAbajo(self, i):
        while (i * 2) <= self.tamanoActual:
            hm = self.hijoMin(i)
            if (self.es_min and self.listaMonticulo[i] > self.listaMonticulo[hm]) or \
               (not self.es_min and self.listaMonticulo[i] < self.listaMonticulo[hm]):
                self.listaMonticulo[i], self.listaMonticulo[hm] = self.listaMonticulo[hm], self.listaMonticulo[i]
            i = hm

    def hijoMin(self, i):
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            if (self.es_min and self.listaMonticulo[i*2] < self.listaMonticulo[i*2+1]) or \
               (not self.es_min and self.listaMonticulo[i*2] > self.listaMonticulo[i*2+1]):
                return i * 2
            else:
                return i * 2 + 1

    def eliminarMin(self):
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual -= 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado

    def construirMonticulo(self, unaLista):
        i = len(unaLista) // 2
        self.tamanoActual = len(unaLista)
        self.listaMonticulo = [0] + unaLista[:]
        while (i > 0):
            self.infiltAbajo(i)
            i -= 1


class MedianaMonticulo:
    """Calcula la mediana de un conjunto de datos usando Monticulos Binarios"""
    
    def __init__(self):
        
        self.minHeap = MonticuloBinario(es_min=True)   # Para la mitad mayor
        self.maxHeap = MonticuloBinario(es_min=False)  # Para la mitad menor

    def insertar(self, valor):
        if self.maxHeap.tamanoActual == 0 or valor < self.maxHeap.listaMonticulo[1]:
            self.maxHeap.insertar(valor)
        else:
            self.minHeap.insertar(valor)
        self.balancear()

    def balancear(self):
        if self.maxHeap.tamanoActual > self.minHeap.tamanoActual + 1:
            self.minHeap.insertar(self.maxHeap.eliminarMin())
        elif self.minHeap.tamanoActual > self.maxHeap.tamanoActual:
            self.maxHeap.insertar(self.minHeap.eliminarMin())

    def obtenerMediana(self):
        if self.maxHeap.tamanoActual > self.minHeap.tamanoActual:
            return self.maxHeap.listaMonticulo[1]
        else:
            return (self.maxHeap.listaMonticulo[1] + self.minHeap.listaMonticulo[1]) / 2.0

    