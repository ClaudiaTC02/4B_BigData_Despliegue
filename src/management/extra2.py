from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.step import MRStep

class Extra2(MRJob):

    def mapper(self, _, line):
        data = line.split(',')

        #fichero XX-XX-XXXX.csv
        if(len(data) == 5):
            empresa=data[0]
            ult_coti=float(data[1].replace(".", "").replace(",", "."))
            yield(empresa, ("coti", ult_coti))
        #fichero informacion_empresas.csv
        if(len(data) == 6):
            empresa=data[0]
            tipo=data[2]
            yield(empresa, ("info", tipo))
            
        
        
        
    def reducer(self, empresa, values):
        cotizacion=0
        tipo_empresa=None
        for tipo, otro  in values:
            if(tipo  == "coti"):
                cotizacion = otro
            if(tipo == 'info'):
                tipo_empresa=otro

        if tipo_empresa is not None and cotizacion != 0:
            yield (tipo_empresa, cotizacion)


    def reducer_find_avg(self, tipo, cotizacion):
        suma=0
        longitud=0
        for i in cotizacion:
            longitud+=1
            suma+=i

        if longitud > 0:
            media_cotizacion = suma / longitud
            yield (None, (tipo, media_cotizacion))


    def reducer_find_max_trend(self, _, values):
        max_trend = max(values, key=lambda x: x[1])
        yield max_trend
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper,reducer=self.reducer),
            MRStep(reducer=self.reducer_find_avg),
            MRStep(reducer=self.reducer_find_max_trend)
        ]

    
if __name__ == '__main__':
    Extra2.run()
