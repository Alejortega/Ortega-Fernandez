import math



class Alimento:
    def __init__(self, peso): #inicializa una instancia de la clase Alimento
        
       
        self.peso = peso

class Fruta(Alimento):
    None  

class Verdura(Alimento):
    None     
#Son de herencia
class Manzana(Fruta):
    def calcular_aw(self):
        C = 15
        m = self.peso
        aw = (0.97 * (((C*m)**2)/(1 + ((C*m)**2))))    
        return round(aw, 2)   

class Kiwi(Fruta):
    def calcular_aw(self):
        C=18
        m=self.peso
        aw = (0.96 * ((1 - ((math.e)**(-C*m)))/ (1 + ((math.e)**(-C*m))) ))       
        return round(aw, 2) 
    
class Papa(Verdura):
    def calcular_aw(self):
        C=18
        m = self.peso
        aw = (0.66 * (math.atan(C*m)))
        return round(aw, 2)

class Zanahoria(Verdura):
    def calcular_aw(self):
        C=10
        m=self.peso
        aw = (0.96 * (1 - ((math.e)**(-C*m)))) 
        return round(aw, 2)   
    



