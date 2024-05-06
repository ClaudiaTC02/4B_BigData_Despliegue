from mrjob.step import MRStep
from mrjob.job import MRJob
import datetime
import calendar

class Semanal(MRJob):
    def mapper(self, _, linea):
        #obtencion valores necesarios
        palabras = linea.split(",")
        accion = palabras[0]
        ultima_coti = float(palabras[1].replace(".", "").replace(",", "."))
        fecha_str = palabras[5]

        yield(accion, (fecha_str, ultima_coti))

    def reducer(self, accion, valores):
        #calculo de los valores de cotizacion y fechas
        cotizaciones = list(valores)
        fecha_ini = cotizaciones[0][0]

        fecha_objeto_ini = datetime.datetime.strptime(fecha_ini, "%d-%m-%Y")
        semana_ini = fecha_objeto_ini - datetime.timedelta(days=fecha_objeto_ini.weekday())
        mes_ini = fecha_objeto_ini.replace(day=1)

        
        #comprobar si pertenecen a la semana/mes o solo al mes
        for fecha_str, ultima_coti in cotizaciones:
            fecha_objeto = datetime.datetime.strptime(fecha_str, "%d-%m-%Y")

            semana_actual = fecha_objeto - datetime.timedelta(days=fecha_objeto.weekday())
            if semana_actual == semana_ini:
                yield ("semana", accion), (fecha_str, ultima_coti)
                
            # Verificar si la fecha está en el mismo mes que fecha_ini
            if fecha_objeto.year == fecha_objeto_ini.year and fecha_objeto.month == fecha_objeto_ini.month:
                yield ("mes", accion), (fecha_str, ultima_coti)

                
    def reducer2(self, tipo_accion, valores):
        valores = list(valores)

        # Ordenar los valores por fecha
        valores.sort(key=lambda x: datetime.datetime.strptime(x[0], "%d-%m-%Y"))

        # Calcular la diferencia para cada acción
        diferencia = valores[-1][1] - valores[0][1]

        # Devolver el tipo (mes o semana), la acción y la diferencia
        yield tipo_accion[0], (tipo_accion[1], diferencia)
        
    def reducer_top5(self, tipo, valores):
        #calculo de las acciones que más han bajado
        top5 = sorted(valores, key=lambda x: x[1], reverse=True)[-5:]
        for accion, diferencia in top5:
            yield tipo, (accion, diferencia)
    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.reducer2),
            MRStep(reducer=self.reducer_top5)
        ]

                         
if __name__ == '__main__':
    Semanal.run()
