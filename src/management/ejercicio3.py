from mrjob.step import MRStep
from mrjob.job import MRJob

class Ejercicio3(MRJob):

    def configure_args(self):
        super(Ejercicio3, self).configure_args()
        self.add_passthru_arg('--accion', default='AENA', help='Introduzca el nombre de una acción)')

    def mapper(self, _, linea):
        accion=self.options.accion
        palabras=linea.split(",")

        nombre=palabras[0]
        if(str(nombre) == str(accion)):
            ultima_coti=float(palabras[1])
            maximo_sesion=float(palabras[2])
            minimo_sesion=float(palabras[3])
            yield(nombre, (ultima_coti, maximo_sesion, minimo_sesion))
                            
        
    def reducer(self, accion, valores):
        cotizaciones = []
        minimos = []
        maximos = []
        for coti, maximo, minimo in valores:
            cotizaciones.append(coti)
            minimos.append(minimo)
            maximos.append(maximo)
            
        # calcular valor minimo de cotización
        valor_minimo = min(minimos)
        # calcular valor máximo de cotización
        valor_maximo = max(maximos)
        
        promedio_cotizaciones = sum(cotizaciones) / len(cotizaciones)

        # calcular el portentaje de decremento desde el valor inicial de cotización hasta el mínimo
        decremento_porcentaje = ((promedio_cotizaciones - valor_minimo) / promedio_cotizaciones) * 100

        # calcular el portentaje de incremento desde el valor inicial de cotización hasta el máximo
        incremento_porcentaje = ((valor_maximo - promedio_cotizaciones) / promedio_cotizaciones) * 100

        yield(accion, (valor_minimo, valor_maximo, decremento_porcentaje, incremento_porcentaje))
  


if __name__ == '__main__':
    Ejercicio3.run()
