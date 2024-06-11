from enum import Enum

class Stanje(Enum):
    MEĐUPOLOŽAJ = "međupoložaj"
    ISKLJUČEN = "isključen"
    UKLJUČEN = "uključen"
    KVAR_SIGNALIZACIJE = "kvar signalizacije"

class StanjeOp(Enum):
    PRORADA = "prorada"
    PRESTANAK = "prestanak"

class Upravljanje(Enum):
    DALJINSKO = "daljinsko" 
    LOKALNO = "lokalno"


class Napon:
    def __init__(self):
        self.powered = True

    def set_power(self, state):
        self.powered = state
        print("Sustav napajanja je ", "uključen." if state else "isključen.")

    def is_powered(self):
        return self.powered


class Sabirnica:
    def __init__(self, id=0, stanje=Stanje.ISKLJUČEN):
        self.id = id
        self.stanje = stanje

    def ukljuci(self):
        self.stanje = Stanje.UKLJUČEN
        print(f"Sabirnica {self.id} uključena.")

    def iskljuci(self):
        self.stanje = Stanje.ISKLJUČEN
        print(f"Sabirnica {self.id} isključena.")


class PrimarnaOprema:
    def __init__(self, stanje=Stanje.UKLJUČEN):
        self.stanje = stanje
        self.napon=Napon() #ima napon

    def komanda(self, ukljuci): 
        #ukljuci = true -> uključenje 
        #ukljuci = false -> isključenje
        if not self.ima_napajanje():
            print(f"{self.__class__.__name__} se ne može uključiti / isključiti, nema napajanja.")
            return None
        self.stanje= Stanje.UKLJUČEN if ukljuci else Stanje.ISKLJUČEN
        return self.stanje

    
    def odredi_polozaj(self):
        return self.stanje
    
    def ima_napajanje(self):
        return self.napon.is_powered()
    
    def nije_nepoznato(self):
        return self.stanje in Stanje
    

class Prekidac(PrimarnaOprema):
    def __init__(self):
        super().__init()
    def dovoljnoSF6():
        return True
    def daljinskoUpravljanje():
        return True

class Rastavljac(PrimarnaOprema):
    def __init__(self, stanje=Stanje.UKLJUČEN):
        super().__init(stanje)

class Zastita:
  
    def nije_u_proradi(self):
        # Get all attributes of the instance
        for attribute_name, attribute_value in self.__dict__.items():
            # Check if any attribute does not equal StanjeOp.PRESTANAK
            if attribute_value != StanjeOp.PRESTANAK:
                return False
        return True
    


class Polje:
    def __init__(self):

        self.prekidac = Prekidac()
        self.i_rastavljac = RIzlazni()
        self.u_rastavljac = RUzemljenja()
    def imaju_napajanje(self):
            for uredaj in [self.prekidac, self.i_rastavljac, self.u_rastavljac, self.s_rastavljacS1, self.s_rastavljacS2]:
                if not uredaj.ima_napajanje():
                    print(f"{uredaj.__class__.__name__} nema napajanje.")
                    return False
            
            return True
    def poznati_polozaji(self):
            for uredaj in [self.prekidac, self.i_rastavljac, self.u_rastavljac, self.s_rastavljacS1, self.s_rastavljacS2]:
                if not uredaj.nije_nepoznato():
                    print(f"{uredaj.__class__.__name__} je u nepoznatom stanju.")
                    return False
            
            return True

    

                
        


class LTB145D1(Prekidac):                   # naslijeđuje klasu Prekidac
    def __init__(self):                     # konstruktor
        super().__init__()                    # konstruktor nad klase: Prekidac

        self.gubitak_sf6 = StanjeOp.PRESTANAK
        self.blokada_rada = StanjeOp.PRESTANAK
        self.blokada_isklopa = StanjeOp.PRESTANAK
        self.opruga_navijena = StanjeOp.PRESTANAK
    
    def dovoljnoSF6(self):
        return self.gubitak_sf6 == StanjeOp.PRESTANAK


class APU(Zastita):
    def __init__(self):
        super().__init__()
        self.ukljucenje = StanjeOp.PRESTANAK
        self.p1 = StanjeOp.PRESTANAK
        self.p3 = StanjeOp.PRESTANAK
        self.blokada = StanjeOp.PRESTANAK

        
        
class Distantna(Zastita):
    def __init__(self):
        super().__init__()
        self.iskljucenje = StanjeOp.PRESTANAK
        self.faza_l1 = StanjeOp.PRESTANAK
        self.faza_l2 = StanjeOp.PRESTANAK
        self.faza_l3 = StanjeOp.PRESTANAK
        self.zemljospoj = StanjeOp.PRESTANAK
        self.kvar = StanjeOp.PRESTANAK
        

class Nadstrujna(Zastita):

    def __init__(self):
        super().__init__()
        self.npc_iskljucenje = StanjeOp.PRESTANAK
        self.vpc_iskljucenje = StanjeOp.PRESTANAK
        self.zemljospojna_iskljucenje = StanjeOp.PRESTANAK
        self.od_preopterecenja_upozorenje = StanjeOp.PRESTANAK
        self.od_preopterecenja_iskljucenje = StanjeOp.PRESTANAK
        self.relej_kvar = StanjeOp.PRESTANAK


class MjerniPretvornik:

    def __init__(self, radna_energija=10, jalova_snaga=10):
        if not isinstance(radna_energija, (int, float)):
            raise ValueError("radna_energija must be a numerical value")
        if not isinstance(jalova_snaga, (int, float)):
            raise ValueError("jalova_snaga must be a numerical value")
        self.radna_energija = radna_energija
        self.jalova_snaga = jalova_snaga
       




class RSabirnicki(Rastavljac):  # naslijeđuje klasu Rastavljac
    def __init__(self, sabirnica):
        super().__init__()
        self.sabirnica = sabirnica  # Lista sabirnica s kojima je rastavljač povezan
        
    def aktiviraj(self):
        self.sabirnica.ukljuci()
        self.komanda(True)
        print("Rastavljač je uključen i sabirnice su aktivne.")
    
    def deaktiviraj(self):
        self.sabirnica.iskljuci()
        self.komanda(False)
        print("Rastavljač je isključen i sabirnice su deaktivirane.") 
        
    def _komanda(self, ukljuci):
        # Private method, not meant to be called directly outside this class
        super().komanda(ukljuci)        
              

class RIzlazni(Rastavljac):     # naslijeđuje klasu Rastavljac
    def __init__(self):
        super().__init__()                     #  nema svojih atributa

class RUzemljenja(Rastavljac):
    def __init(self, state=Stanje.ISKLJUČEN):
        super().__init__(state)
        
    



class DalekovodnoPolje(Polje):                                  # naslijeđuje klasu Polje
    def __init__(self): # konstruktor
        super().__init__()  # konstruktor nad klase: Polje
   
        self.dist_zastita = Distantna()
        self.nads_zastita = Nadstrujna()                        # abstraktna: klasa Zastita/Nadstrujna
        self.apu = APU()                                          # klasa: APU    
        self.mjera = MjerniPretvornik()                                      # klasa: MjerniPretvornik
        self.grupni_iskljucenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)
        self.grupni_upozorenje = StanjeOp.PRESTANAK             # klasa: StanjeOp (enum vrijednost)
        self.grupni_smetnje = StanjeOp.PRESTANAK                # klasa: StanjeOp (enum vrijednost)

    def zastita_nije_u_proradi(self):
        for zastita in [self.dist_zastita, self.nads_zastita, self.apu]:
            if not zastita.nije_u_proradi():
                print(f"{zastita.__class__.__name__} je u proradi.")
                return False
        return True
    
        
    
    def spremno(self):
        if not self.zastita_nije_u_proradi():
            print("Zašita je u proradi. Dalekovodno polje nije spremno.")
            return False
        if not self.imaju_napajanje():
            print("Nemaju svi sklopni aparati napajanje. Dalekovodno polje nije spremno")
            return False
        if not self.prekidac.dovoljnoSF6():
            print("Razina plina SF6 je preniska. Dalekovodno polje nije spremno.")
            return False
        if not self.prekidac.daljinskoUpravljanje():
            print("Daljinsko upravljanje nije omogućeno. Dalekovodno polje nije spremno.")
            return False
        if not self.poznati_polozaji():
            print("Jedan od sklopnih aparata je u nepoznatom položaju. Potrebno je poslati osoblje u rasklopno postrojenje")
            print("Dalekovodno polje nije spremno")
            return False
        return True

class Dalekovodno2Sab(DalekovodnoPolje):
    def __init__(self):
        super().__init__()

        self.sabirnicaS1=Sabirnica(1)
        self.s_rastavljacS1=RSabirnicki(self.sabirnicaS1)
        self.sabirnicaS2=Sabirnica(2)
        self.s_rastavljacS2=RSabirnicki(self.sabirnicaS2, Stanje.UKLJUČEN)
        self.S_polje=SpojnoPolje(self.s_rastavljacS1, self.s_rastavljacS2)
        
    def prespoji(self):
        # Control the SpojnoPolje to switch to the new busbar
        self.S_polje.ukljuci()
        self.S_polje.prespoji()
        self.S_polje.iskljuci()
        if self.sabirnicaS1.stanje == Stanje.UKLJUČEN:
            print("Spojeno na S1")
        elif self.sabirnicaS2.stanje == Stanje.UKLJUČEN:
            print("Spojeno na S2")

        
        
class Dalekovodno1Sab(DalekovodnoPolje):
    def __init__(self):
        super().__init__()

        self.sabirnica=Sabirnica()
        self.s_rastavljac=RSabirnicki(self.sabirnica)
    def imaju_napajanje(self):
        for uredaj in [self.prekidac, self.i_rastavljac, self.u_rastavljac, self.s_rastavljac]:
            if not uredaj.ima_napajanje():
                print(f"{uredaj.__class__.__name__} nema napajanje.")
                return False
                
        return True
    def poznati_polozaji(self):
        for uredaj in [self.prekidac, self.i_rastavljac, self.u_rastavljac, self.s_rastavljac]:
            if not uredaj.nije_nepoznato():
                print(f"{uredaj.__class__.__name__} je u nepoznatom stanju.")
                return False
            
        return True




class TPKoncar(Prekidac):                           # naslijeđuje klasu Prekidac 
    def __init__(self):  # konstruktor
        super().__init__()                    # konstruktor nad klase: Prekidac
        
        self.pad_tlaka_16b = StanjeOp.PRESTANAK    

        self.pad_tlaka_14b = StanjeOp.PRESTANAK
        self.pad_tlaka_11b = StanjeOp.PRESTANAK
        self.apu_blokada = StanjeOp.PRESTANAK
        self.nesklad_polova_3p_isklop = StanjeOp.PRESTANAK
        self.upravljanje = Upravljanje.DALJINSKO
    
    
    def daljinskoUpravljanje(self):
        return self.upravljanje == Upravljanje.DALJINSKO
    

        


class Dalekovod:
    def __init__(self):
        self.D_polje1 = Dalekovodno1Sab()
        self.D_polje2 = Dalekovodno2Sab()
    
    
    def ukljuci(self):
        for polje in [self.D_polje1, self.D_polje2]:
            if not polje.spremno():
                print("Stoga se dalekovod ne može uključiti.")
                return
            polje.u_rastavljac.komanda(False)
            for rastavljac in polje.s_rastavljaci:
                rastavljac.komanda(True)
            polje.i_rastavljac.komanda(True)
            polje.prekidac.komanda(True)
        
        print("Dalekovod uključen")

    def iskljuci(self):
        for polje in [self.D_polje1, self.D_polje2]:
            if not polje.spremno():
                print("Stoga se dalekovod ne može isključiti.")
                return
            polje.prekidac.komanda(False)
            for rastavljac in polje.s_rastavljaci:
                rastavljac.komanda(False)
            polje.i_rastavljac.komanda(False)
            polje.u_rastavljac.komanda(True)
            
            
            
        print("Dalekovod isključen")

class SpojnoPolje(Polje):                                      # naslijeđuje klasu Polje 
    def __init__(self, s_rastavljacS1, s_rastavljacS2, stanje=Stanje.ISKLJUČEN):  # konstruktor
        super().__init__() # konstruktor nad klase: Polje
        self.grupni_iskljucenje = StanjeOp.PRESTANAK           # klasa: StanjeOp (enum vrijednost) 
        self.grupni_upozorenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)  
        self.grupni_smetnje = StanjeOp.PRESTANAK               # klasa: StanjeOp (enum vrijednost)
        self.stanje=stanje
        self.s_rastavljacS1 = s_rastavljacS1
        self.s_rastavljacS2 = s_rastavljacS2

    def ukljuci(self):
        # Turn on the switch
        for rastavljac in [self.s_rastavljacS1, self.s_rastavljacS2]:
                rastavljac.aktiviraj()
        
        self.prekidac.komanda(True)


    def iskljuci(self):
        # Turn off everything when switching is done
        self.prekidac.komanda(False)
        for rastavljac in [self.s_rastavljacS1, self.s_rastavljacS2]:
            rastavljac.deaktiviraj()
    
    def prespoji(self):
        if self.s_rastavljacS1.odredi_polozaj() == Stanje.UKLJUČEN and self.s_rastavljacS2.odredi_polozaj() == Stanje.ISKLJUČEN:
            self.s_rastavljacS1.deaktiviraj()
            self.s_rastavljacS2.aktiviraj()
        else:
            self.s_rastavljacS1.aktiviraj()
            self.s_rastavljacS2.deaktiviraj()
    def spremno(self):
        if not self.imaju_napajanje():
            print("Nemaju svi sklopni aparati napajanje. Spojno polje nije spremno")
            return False
        if not self.prekidac.dovoljnoSF6():
            print("Razina plina SF6 je preniska. Spojno polje nije spremno.")
            return False
        if not self.prekidac.daljinskoUpravljanje():
            print("Daljinsko upravljanje nije omogućeno. Polje nije spremno.")
            return False
        if not self.poznati_polozaji():
            print("Jedan od sklopnih aparata je u nepoznatom položaju. Potrebno je poslati osoblje u rasklopno postrojenje")
            print("Polje nije spremno")
            return False
        return True
            
