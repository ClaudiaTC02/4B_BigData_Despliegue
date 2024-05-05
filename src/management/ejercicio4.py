from mrjob.step import MRStep
from mrjob.job import MRJob
import datetime
import time

class Ejercicio4(MRJob):
    
    def configure_args(self):
        super(Ejercicio4, self).configure_args()
        self.add_passthru_arg('--accion', default='AENA', help='Introduzca el nombre de una acción)')

    def mapper(self, _, linea):
        
        accion=self.options.accion
        palabras=linea.split(",")

        nombre=palabras[0]
        if(str(nombre) == str(accion)):
            maximo_sesion=float(palabras[2].replace(".", "").replace(",", "."))
            minimo_sesion=float(palabras[3].replace(".", "").replace(",", "."))
            hora=palabras[4]
            fecha=palabras[5]
            yield(nombre, (maximo_sesion, minimo_sesion, fecha, hora))
                            
        
    def reducer(self, accion, valores):
        minimos = []
        minimos_semana = []
        minimos_hora = []
        maximos = []
        maximos_semana = []
        maximos_hora = []

        fecha_actual=datetime.datetime.now()
        fecha_actual_unix = int(fecha_actual.timestamp())
        
        fecha_ayer= fecha_actual - datetime.timedelta(days=1)
        fecha_ayer_unix = int(fecha_ayer.timestamp())

        una_semana_atras = fecha_actual - datetime.timedelta(weeks=1)
        una_semana_atras_unix = int(una_semana_atras.timestamp())
        
        for maximo, minimo, fecha_archivo, hora in valores:
            minimos.append(minimo)
            maximos.append(maximo)

            fecha = datetime.datetime.strptime(str(fecha_archivo), "%d-%m-%Y")
            fecha_archivo_unix=int(fecha.timestamp())
            if(fecha_archivo_unix >= una_semana_atras_unix and fecha_archivo_unix <= fecha_actual_unix):
                minimos_semana.append(minimo)
                maximos_semana.append(maximo)

            if(fecha_archivo_unix >= fecha_ayer_unix and fecha_archivo_unix <= fecha_actual_unix):
                hora_actual = datetime.datetime.now().hour
                hora_anterior = (datetime.datetime.now() - datetime.timedelta(hours=1)).hour
                hora_dt = datetime.datetime.strptime(hora, "%H:%M").hour
                
                # Corregir la hora anterior si es 0 (medianoche) 
                if hora_anterior == 0:
                    hora_anterior = 24
                # Corregir la hora actual si es 0 (medianoche) 
                if hora_actual == 0:
                    hora_actual = 24
                # Corregir la hora del archivo si es 0 (medianoche) 
                if hora_dt == 0:
                    hora_dt = 24

                if(hora_dt >= hora_anterior and hora_dt <= hora_actual):
                    minimos_hora.append(minimo)
                    maximos_hora.append(maximo)

        # -------------- mes --------------

        try:
            # calcular valor minimo de cotización
            valor_minimo_mes = min(minimos)
            # calcular valor máximo de cotización
            valor_maximo_mes = max(maximos)       
        except ValueError:
            valor_minimo_mes="??"
            valor_maximo_mes="??"

        # -------------- semana --------------

        try:
            # calcular valor minimo de cotización
            valor_minimo_semana = min(minimos_semana)
            # calcular valor máximo de cotización
            valor_maximo_semana = max(maximos_semana)
        except ValueError:
            valor_minimo_semana="??"
            valor_maximo_semana="??"

        # -------------- hora --------------

        try:
            # calcular valor minimo de cotización
            valor_minimo_hora = min(minimos_hora)
            # calcular valor máximo de cotización
            valor_maximo_hora = max(maximos_hora)
        except ValueError:
            valor_minimo_hora="??"
            valor_maximo_hora="??"
        
        yield(accion, (valor_minimo_mes, valor_maximo_mes, valor_minimo_semana, valor_maximo_semana, valor_minimo_hora, valor_maximo_hora))
  


if __name__ == '__main__':
    Ejercicio4.run()
