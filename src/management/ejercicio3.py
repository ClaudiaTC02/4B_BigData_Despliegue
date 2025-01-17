from mrjob.step import MRStep
from mrjob.job import MRJob
import datetime

class Ejercicio3(MRJob):

    def configure_args(self):
        super(Ejercicio3, self).configure_args()
        self.add_passthru_arg('--accion', default='AENA', help='Introduzca el nombre de una acción)')

    def mapper(self, _, linea):
        accion=self.options.accion
        palabras=linea.split(",")

        nombre=palabras[0]
        if(str(nombre) == str(accion)):
            ultima_coti=float(palabras[1].replace(".", "").replace(",", "."))
            fecha=palabras[5]
            maximo_sesion=float(palabras[2].replace(".", "").replace(",", "."))
            minimo_sesion=float(palabras[3].replace(".", "").replace(",", "."))
            yield(nombre, (fecha, ultima_coti, maximo_sesion, minimo_sesion))
                            
        
    def reducer(self, accion, valores):

        cotizaciones = list(valores)

        minimos = [minimo[3] for minimo in cotizaciones]
        maximos = [maximo[2] for maximo in cotizaciones]
        # calcular valor minimo de cotización
        valor_minimo = min(minimos)
        # calcular valor máximo de cotización
        valor_maximo = max(maximos)

        # Ordenar cotizaciones por fecha
        cotizaciones.sort(key=lambda x: datetime.datetime.strptime(x[0], "%d-%m-%Y"))
        cotizacion_inicial = cotizaciones[0][1]

        # calcular el portentaje de decremento desde el valor inicial de cotización hasta el mínimo
        decremento_porcentaje = ((cotizacion_inicial - valor_minimo) / cotizacion_inicial) * 100

        # calcular el portentaje de incremento desde el valor inicial de cotización hasta el máximo
        incremento_porcentaje = ((valor_maximo - cotizacion_inicial) / cotizacion_inicial) * 100

        yield(accion, (valor_minimo, valor_maximo, decremento_porcentaje, incremento_porcentaje))
  


if __name__ == '__main__':
    Ejercicio3.run()
