from mrjob.step import MRStep
from mrjob.job import MRJob
import datetime

class Ejercicio7(MRJob):

    def configure_args(self):
        super(Ejercicio7, self).configure_args()
        self.add_passthru_arg('--porcentaje', default='AENA', help='Introduzca el nombre de una acción)')

    def mapper(self, _, linea):
        palabras=linea.split(",")

        nombre=palabras[0]
        ultima_coti=float(palabras[1].replace(".", "").replace(",", "."))
        fecha=palabras[5]
        yield(nombre, (fecha, ultima_coti))
                            
        
    def reducer(self, accion, valores):

        cotizaciones = list(valores)

        # Ordenar cotizaciones por fecha
        cotizaciones.sort(key=lambda x: datetime.datetime.strptime(x[0], "%d-%m-%Y"))
        cotizacion_inicial = float(cotizaciones[0][1])
        cotizacion_final = float(cotizaciones[-1][1])

        incremento_porcentaje = ((cotizacion_final - cotizacion_inicial) / cotizacion_inicial) * 100

        if(round(incremento_porcentaje) == float(self.options.porcentaje)):
            yield(accion, (incremento_porcentaje, self.options.porcentaje))
  


if __name__ == '__main__':
    Ejercicio7.run()
