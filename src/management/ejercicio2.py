from mrjob.step import MRStep
from mrjob.job import MRJob
import datetime

class Mensual(MRJob):

    def mapper(self, _, linea):
        #obetener los datos necesarios para el reducer
        palabras=linea.split(",")
        ultima_coti=float(palabras[1].replace(".", "").replace(",", "."))
        fecha=palabras[5]
        maximo_sesion=float(palabras[2].replace(".", "").replace(",", "."))
        minimo_sesion=float(palabras[3].replace(".", "").replace(",", "."))
        
        yield(palabras[0], (fecha, ultima_coti, maximo_sesion, minimo_sesion))
                            
        
    def reducer(self, accion, valores):
        cotizaciones = list(valores)
        #cálculo de los valores máximos y mínimos
        minimos = [minimo[3] for minimo in cotizaciones]
        maximos = [maximo[2] for maximo in cotizaciones]
        # calcular valor minimo de cotización
        valor_minimo = min(minimos)
        # calcular valor máximo de cotización
        valor_maximo = max(maximos)
        
        # Ordenar cotizaciones por fecha
        cotizaciones.sort(key=lambda x: datetime.datetime.strptime(x[0], "%d-%m-%Y"))
        #cálculo del valor inicial y final de cotización
        cotizacion_inicial = cotizaciones[0][1]
        cotizacion_final = cotizaciones[-1][1]
        
        yield(accion, (cotizacion_inicial, cotizacion_final, valor_minimo, valor_maximo))
            


if __name__ == '__main__':
    Mensual.run()
