from abc import  ABC, abstractmethod
from fpdf import FPDF


#definición de la clase PDF para manejar la creación de PDF
class PDF(FPDF):

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte ', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln(10)


class BaseReporte(ABC):
    """CLase abstracta que define los métodos que deben implementar las clases derivadas"""

    @abstractmethod
    def generar_reporte(self, reclamos, med_proceso, med_resueltos):
        pass

    @abstractmethod
    def agregar_titulo(self, titulo):
        pass

    @abstractmethod
    def agregar_texto(self, texto):
        pass

    @abstractmethod
    def agregar_imagen(self, ruta_imagen, x, y, w):
        pass


class ReportePDF(BaseReporte):

    """Crea un reporte en formato pdf"""

    def __init__(self):
        self.pdf = PDF()
        

    def generar_reporte(self, reclamos, mediana_proceso, mediana_resueltos):
        self.pdf.add_page()
        self.agregar_titulo("Informe de Reclamos del Departamento")
        self.agregar_texto(f"Cantidad de Reclamos: {reclamos}")
        self.agregar_texto(f"Mediana en Proceso: {mediana_proceso}")
        self.agregar_texto(f"Mediana de Resueltos: {mediana_resueltos}")
        self.agregar_imagen('./static/grafico_torta.png', x=80, y=100, w=80)
        self.agregar_imagen('./static/nube_palabras.png', x=10, y=100, w=80)
        self.pdf.output('./static/reporte.pdf')

    def agregar_titulo(self, titulo):
        self.pdf.chapter_title(titulo)

    def agregar_texto(self, texto):
        self.pdf.chapter_body(texto)

    def agregar_imagen(self, ruta_imagen, x, y, w):
        self.pdf.image(ruta_imagen, x=x, y=y, w=w)

        #self.pdf.output('./static/reporte.pdf')

class ReporteHTML(BaseReporte):
    
    """Crea un reporte en formato html"""

    def __init__(self):
        self.html = ""

    def generar_reporte(self, reclamos, mediana_proceso, mediana_resueltos):
        self.agregar_titulo("Informe de Reclamos del Departamento")
        self.agregar_texto(f"Total de Reclamos: {reclamos}")
        self.agregar_texto(f"Mediana en Proceso: {mediana_proceso}")
        self.agregar_texto(f"Mediana de Resueltos: {mediana_resueltos}")
        self.agregar_imagen('./static/grafico_torta.png', 400, 'auto')
        self.agregar_imagen('./static/nube_palabras.png', 400, 'auto')
        with open('./static/reporte.html', 'w') as file:
            file.write(self.html)

    def agregar_titulo(self, titulo):
        self.html += f"<h1>{titulo}</h1>\n"

    def agregar_texto(self, texto):
        self.html += f"<p>{texto}</p>\n"

    def agregar_imagen(self, ruta_imagen,w, h):
        self.html += f"<img src='{ruta_imagen}'style='width: {w}px; height: {h};'>" 