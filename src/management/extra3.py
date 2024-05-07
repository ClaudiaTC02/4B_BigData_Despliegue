from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.step import MRStep

class Extra3(MRJob):

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
            anyo=int(data[1])
            yield(empresa, ("info", anyo))
            
        
        
        
    def reducer(self, empresa, values):
        cotizacion=[]
        empresa_requisito=None
        for tipo, otro  in values:
            if(tipo  == "coti"):
                cotizacion.append(otro)
            if(tipo == 'info'):
                if(otro < 2000):
                    empresa_requisito=empresa


        if cotizacion:
            cotizacion_inicial=cotizacion[0]
            cotizacion_final=cotizacion[-1]
            incremento_cotizacion=((cotizacion_final-cotizacion_inicial)/cotizacion_inicial)*100
            if empresa_requisito is not None and incremento_cotizacion != 0:
                yield (None,(empresa, incremento_cotizacion))


    def reducer_find_min_coti(self, _, values):
        nombre=None
        minimo=100
        for empresa,incremento in values:
            if(incremento < minimo):
                minimo=incremento
                nombre=empresa
                
        yield (nombre, minimo)
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper,reducer=self.reducer),
            MRStep(reducer=self.reducer_find_min_coti)
        ]

    
if __name__ == '__main__':
    Extra3.run()
