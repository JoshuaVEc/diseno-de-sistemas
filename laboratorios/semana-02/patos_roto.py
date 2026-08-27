
class ComportamientoDeVuelo:

    def volar(self):
        """Define el comportamiento de vuelo de un pato."""
        raise NotImplementedError

class ComportamientoDeGraznido:
    def graznar(self):
        """Define el comportamiento del graznido de un pato."""
        raise NotImplementedError

class GraznidoNormal(ComportamientoDeGraznido):
    def graznar(self):
        print("CuaK");

class GraznidoGoma(ComportamientoDeGraznido):
    def graznar(self):
        print("Chirrido de Goma")

class VuelaConAlas(ComportamientoDeVuelo):
    def volar(self):
        print( "Volando con alas.")


















class NoVuela(ComportamientoDeVuelo):
    def volar(self):
        print( "No puede volar.")


class Pato:
    def __init__(self, comportamiento_vuelo, Comportamiendo_graznido):
        self.comportamiento_vuelo = comportamiento_vuelo
        self.comportamiento_graznido = Comportamiendo_graznido

    def nadar(self):
        print("Nadando.")

    
        
    def volar(self):
        self.comportamiento_vuelo.volar()

    def graznar(self):
        self.comportamiento_graznido.graznar();



class PatoSalvaje(Pato):
    def __init__(self):
        vuela_alas= VuelaConAlas();
        granizo_normal= GraznidoNormal()
        super().__init__(vuela_alas,granizo_normal)
    
        

class PatoDeGoma(Pato):

    def __init__(self):
        no_vuela= NoVuela()
        granizo_de_goma=GraznidoGoma()
        super().__init__(no_vuela,granizo_de_goma)
        

    
    


if __name__ == "__main__":
    salvaje = PatoSalvaje()
    salvaje.volar()
    salvaje.nadar()
    salvaje.graznar()
    
    

    print()
    goma = PatoDeGoma()
    goma.volar()
    goma.nadar()
    goma.graznar()
   
