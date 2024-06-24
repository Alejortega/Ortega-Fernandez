import nltk
import collections
import operator

nltk.download('stopwords')
stopwords_es = nltk.corpus.stopwords.words('spanish')

def reclamos_similares(reclamos_same_depto, texto_objetivo):
    """Devuelve una lista con los IDs de los reclamos similares. Si no los hay, devuelve una lista vacía"""

    similares = []
    lista_objetivo = []
    lista_comparacion = []

    # Filtrar palabras del texto objetivo
    palabras_filtradas_objetivo = [palabra for palabra in texto_objetivo.split() if palabra.lower() not in stopwords_es]
    counter1 = collections.Counter(palabras_filtradas_objetivo)
    lista_objetivo = [palabra for palabra, _ in counter1.most_common()]

    # Filtrar palabras de los textos del mismo departamento
    for reclamo in reclamos_same_depto:
        descripcion = reclamo.get('contenido', '')  # Obtener la descripción del reclamo, si está presente
        if not descripcion:
            continue  # Saltar el reclamo si no tiene contenido

        palabras_filtradas = [palabra for palabra in descripcion.split() if palabra.lower() not in stopwords_es]
        counter = collections.Counter(palabras_filtradas)
        lista_reclamo = [palabra for palabra, _ in counter.most_common()]
        lista_comparacion.append((lista_reclamo, reclamo.get('id')))  # Obtener el ID del reclamo, si está presente

    #comparar palabras significativas
    for lista_reclamo, id_reclamo in lista_comparacion:
        cont = sum(1 for palabra in lista_objetivo if palabra in lista_reclamo)
        prom = (cont / len(lista_objetivo)) * 100
        prom2 = (cont / len(lista_reclamo)) * 100
        if prom >= 40 and prom2 >= 35:
            similares.append((id_reclamo, prom))
    
    similares.sort(key=operator.itemgetter(1), reverse=True)
    lista_IDs = [id_reclamo for id_reclamo, _ in similares]

    return lista_IDs



