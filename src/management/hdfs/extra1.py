from mrjob.job import MRJob
from mrjob.step import MRStep
import os
import re

class Extra1(MRJob):

    def mapper(self, _, line):
        data = line.split(',')
        file_name=os.environ['map_input_file'].split("/")[-1]

        # Expresión regular para verificar el formato DD-MM-YYYY.csv
        pattern = r'\d{2}-\d{2}-\d{4}\.csv$'

        #fichero XX-XX-XXXX.csv
        if re.match(pattern, file_name):
            empresa=data[0]
            ult_coti=float(data[1].replace(".", "").replace(",", "."))
            yield(empresa, ("coti", ult_coti))
        #fichero informacion_empresas.csv
        if(file_name == 'informacion_empresas.csv'):
            empresa=data[0]
            beneficio = float(data[4].replace('M', ''))*1000000
            yield(empresa, ("info",beneficio))
            
        
        
        
    def reducer(self, empresa, values):
        cotizacion=[]
        beneficio=0
        for tipo, otro  in values:
            if(tipo  == "coti"):
                cotizacion.append(otro)
            if(tipo == 'info'):
                beneficio=otro

        if cotizacion and beneficio != 0:
            cotizacion_fin = cotizacion[-1]
            ratio = cotizacion_fin / beneficio
            yield (None,(ratio, empresa))


    def reducer_ranking(self, _, values):
        sorted_values = sorted(values, key=lambda x: x[0], reverse=True)
        rank = 1
        for ratio, empresa in sorted_values:
            yield rank, (empresa, ratio)
            rank += 1


    def steps(self):
        return [
            MRStep(mapper=self.mapper,reducer=self.reducer),
            MRStep(reducer=self.reducer_ranking)
        ]

    
if __name__ == '__main__':
    Extra1.run()
