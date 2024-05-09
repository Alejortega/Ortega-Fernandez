
#clase detectaralimento, venía con el código de la cátedra, devuelve un gráfico
"""X
if __name__ == "__main__":
    
    random.seed(1)
    sensor = DetectorAlimento()
    lista_pesos = []
    for _ in range(200):
        lista_pesos.append(sensor.detectar_alimento()["peso"])

    plt.hist(lista_pesos, bins=12)
    plt.show()
"""

from modules.config import app
from flask import  render_template, request
from Actividad_2.modules.clases1 import *
from Actividad_2.modules.clases2 import CintaTransportadora, CalculadoraAws

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargar_cajon', methods=['POST'])
def cargar_cajon(): 
    
    cantidad = int(request.form['cantidad'])
        
#Creamos instancias de las clases:

    cinta = CintaTransportadora()
    
    cajon = cinta.cargar_cajon(cantidad)  #Cargamos el cajón con alimentos      
    
    calculadora = CalculadoraAws() #Creamos una instancia de CalculadoraAws con el cajón

#Llamamos los métodos:
    promedios = {}
    alimento_alerta = []
    alerta = False
    for alimento in [Manzana, Kiwi, Papa, Zanahoria]:
        promedio = calculadora.calculadora_aws(cajon, alimento)
        promedios[alimento.__name__] = promedio
        if promedio > 0.90:
            alerta = True
            alimento_alerta.append(alimento.__name__) # Guarda en una lista el/los alimentos que superaron para informarlos
    
    #Calculamos los promedios generales
    aw_prom_Fruta = calculadora.calculadora_aws(cajon, Fruta)
    aw_prom_Verdura = calculadora.calculadora_aws(cajon, Verdura)
    aw_prom_total = calculadora.calculadora_aws(cajon, Alimento)
    peso = calculadora.peso_total(cajon)

    return render_template('resultado.html', cajon=cajon, fruta=aw_prom_Fruta, verdura=aw_prom_Verdura, promedios=promedios, 
                           promedio_total=aw_prom_total, peso_cajon=peso, alerta=alerta, alimento_alerta=alimento_alerta)

#No es necesario el "print(cajón)", como tampoco lo que muestra la template resultado que dice "Información de la carga"
#Es para ver si las cálculos de los promedios y el número de alimentos en el cajón estan bien 
      
if __name__ == '__main__':
    app.run(debug=True)


