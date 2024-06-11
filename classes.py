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
    def __init__(self, id, stanje=Stanje.ISKLJUČEN):
        self.id = id
        self.stanje = stanje

    def ukljuci(self):
        self.stanje = Stanje.UKLJUČEN
        print(f"Sabirnica {self.id} uključena.")

    def iskljuci(self):
        self.stanje = Stanje.ISKLJUČEN
        print(f"Sabirnica {self.id} isključena.")


class PrimarnaOprema:
    def __init__(self, stanje):
        self.stanje = stanje
        self.napon=Napon() #ima napon

    def komanda(self, ukljuci): 
        #ukljuci = true -> uključenje 
        #ukljuci = false -> isključenje
        if not self.napon.is_powered():
            print(f"{self.__class__.__name__} se ne može uključiti / isključiti, nema napajanja.")
            return None
        self.stanje=ukljuci
        return self.stanje

    
    def odredi_polozaj(self):
        return self.stanje
    
    def ima_napajanje(self):
        return self.napon.is_powered()
    
    def nije_nepoznato(self):
        return self.stanje in Stanje
    

class Prekidac(PrimarnaOprema):
    def dovoljnoSF6():
        return True
    def daljinskoUpravljanje():
        return True

class Rastavljac(PrimarnaOprema):
    pass

class Zastita:
  
    def nije_u_proradi(self):
        # Get all attributes of the instance
        for attribute_name, attribute_value in self.__dict__.items():
            # Check if any attribute does not equal StanjeOp.PRESTANAK
            if attribute_value != StanjeOp.PRESTANAK:
                return False
        return True
    


class Polje:
    def __init__(self, prekidac, i_rastavljac, u_rastavljac, sabirnice):
        if not isinstance(prekidac, Prekidac):
            raise TypeError("prekidac must be an instance of Prekidac")
        if not isinstance(i_rastavljac, RIzlazni):
            raise TypeError("i_rastavljac must be an instance of RIzlazni")
        if not isinstance(u_rastavljac, RUzemljenja):
            raise TypeError("u_rastavljac must be an instance of RUzemljenja")
        for i in len(sabirnice):
            if not isinstance(sabirnice[i], Sabirnica):
                raise TypeError("every element of sabirnice must be an instance of Sabirnica")
        self.prekidac = prekidac
        self.sabirnice = sabirnice  # Lista sabirnica povezanih s ovim poljem
        self.s_rastavljaci = []
        self.i_rastavljac = i_rastavljac
        self.u_rastavljac = u_rastavljac
        for sabirnica in self.sabirnice:
            self.s_rastavljaci.append(RSabirnicki(sabirnica))
            
    def imaju_napajanje(self):
        for uredaj in [self.prekidac, self.i_rastavljac, self.u_rastavljac]:
            if not uredaj.ima_napajanje():
                print(f"{uredaj.__class__.__name__} nema napajanje.")
                return False
        for rastavljac in self.s_rastavljaci:
            if not rastavljac.ima_napajanje():
                print(f"{rastavljac.__class__.__name__} nema napajanje.")
                return False
        return True
    
    def poznati_polozaji(self):
        for uredaj in [self.prekidac, self.i_rastavljac, self.u_rastavljac]:
            if not uredaj.nije_nepoznato():
                print(f"{uredaj.__class__.__name__} je u nepoznatom položaju.")
                return False
        for rastavljac in self.s_rastavljaci:
            if not rastavljac.nije_nepoznato():
                print(f"{rastavljac.__class__.__name__} je u nepoznatom položaju.")
                return False
        return True
    def spremno(self):
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
        
        


class LTB145D1(Prekidac):                   # naslijeđuje klasu Prekidac
    def __init__(self, stanje):                     # konstruktor
        super().__init__(stanje)                    # konstruktor nad klase: Prekidac

        self.gubitak_sf6 = StanjeOp.PRESTANAK
        self.blokada_rada = StanjeOp.PRESTANAK
        self.blokada_isklopa = StanjeOp.PRESTANAK
        self.opruga_navijena = StanjeOp.PRESTANAK
    
    def dovoljnoSF6(self):
        return self.gubitak_sf6 == StanjeOp.PRESTANAK


class APU(Zastita):
    def __init__(self):
        
        self.ukljucenje = StanjeOp.PRESTANAK
        self.p1 = StanjeOp.PRESTANAK
        self.p3 = StanjeOp.PRESTANAK
        self.blokada = StanjeOp.PRESTANAK

        
        
class Distantna(Zastita):
    def __init__(self):
        
        self.iskljucenje = StanjeOp.PRESTANAK
        self.faza_l1 = StanjeOp.PRESTANAK
        self.faza_l2 = StanjeOp.PRESTANAK
        self.faza_l3 = StanjeOp.PRESTANAK
        self.zemljospoj = StanjeOp.PRESTANAK
        self.kvar = StanjeOp.PRESTANAK
        

class Nadstrujna(Zastita):

    def __init__(self):
        
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
    def __init__(self, sabirnica, stanje=Stanje.ISKLJUČEN):
        super().__init__(stanje)
        self.sabirnica = sabirnica  # Lista sabirnica s kojima je rastavljač povezan
    
    def aktiviraj(self):
        self.sabirnica.ukljuci()
        self.stanje = True
        print("Rastavljač je uključen i sabirnice su aktivne.")
    
    def deaktiviraj(self):
        self.sabirnica.iskljuci()
        self.stanje = False
        print("Rastavljač je isključen i sabirnice su deaktivirane.")                        #  nema svojih atributa

class RIzlazni(Rastavljac):     # naslijeđuje klasu Rastavljac
    pass                        #  nema svojih atributa

class RUzemljenja(Rastavljac):
    pass



class DalekovodnoPolje(Polje):                                  # naslijeđuje klasu Polje
    def __init__(self, prekidac, sabirnice, i_rastavljac, u_rastavljac, dist_zastita, nads_zastita, apu, mjera, S_polje=None): # konstruktor
        super().__init__(prekidac, i_rastavljac, u_rastavljac, sabirnice)  # konstruktor nad klase: Polje
        if not isinstance(dist_zastita, Distantna):
            raise TypeError("dist_zastita must be an instance of Distantna")
        if not isinstance(nads_zastita, Nadstrujna):
            raise TypeError("nads_zastita must be an instance of Nadstrujna")
        if not isinstance(apu, APU):
            raise TypeError("apu must be an instance of APU")  
        if not isinstance(mjera, MjerniPretvornik):
            raise TypeError("mjera must be an instance of MjerniPretvornik")  
        if S_polje is not None and not isinstance(S_polje, SpojnoPolje):
            raise TypeError("S_polje, if provided, must be an instance of SpojnoPolje")
        self.dist_zastita = dist_zastita
        self.nads_zastita = nads_zastita                        # abstraktna: klasa Zastita/Nadstrujna
        self.apu = apu                                          # klasa: APU    
        self.mjera = mjera                                      # klasa: MjerniPretvornik
        self.grupni_iskljucenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)
        self.grupni_upozorenje = StanjeOp.PRESTANAK             # klasa: StanjeOp (enum vrijednost)
        self.grupni_smetnje = StanjeOp.PRESTANAK                # klasa: StanjeOp (enum vrijednost)
        self.S_polje=S_polje
    
    def prespoji(self, nova_sabirnica):
        # Control the SpojnoPolje to switch to the new busbar
        self.S_polje.ukljuci()
        
        for rastavljac in self.s_rastavljaci:
            if rastavljac.sabirnica == nova_sabirnica:
                rastavljac.aktiviraj()
            else:
                rastavljac.deaktiviraj()
        self.S_polje.iskljuci()
        print(f"Dalekovodno polje prespojeno na {nova_sabirnica.id} preko spojnog polja.")
        
        
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
        



class TPKoncar(Prekidac):                           # naslijeđuje klasu Prekidac 
    def __init__(self, stanje, upravljanje, tlak):  # konstruktor
        super().__init__(stanje)                    # konstruktor nad klase: Prekidac
        
        self.pad_tlaka_16b = StanjeOp.PRESTANAK    

        self.pad_tlaka_14b = StanjeOp.PRESTANAK
        self.pad_tlaka_11b = StanjeOp.PRESTANAK
        self.apu_blokada = StanjeOp.PRESTANAK
        self.nesklad_polova_3p_isklop = StanjeOp.PRESTANAK
        self.upravljanje = upravljanje
    
    
    def daljinskoUpravljanje(self):
        return self.upravljanje == Upravljanje.DALJINSKO
    

        


class Dalekovod:
    def __init__(self, D_polje1, D_polje2):
        if not isinstance(D_polje1, DalekovodnoPolje) or not isinstance(D_polje2, DalekovodnoPolje):
            raise TypeError("Both D_polje1 and D_polje2 must be instances of DalekovodnoPolje")
        self.D_polje1 = D_polje1
        self.D_polje2 = D_polje2
    
    
    def ukljuci(self):
        print("Dalekovod uključen")

    def iskljuci(self):
        print("Dalekovod isključen")

class SpojnoPolje(Polje):                                      # naslijeđuje klasu Polje 
    def __init__(self, prekidac, i_rastavljac, u_rastavljac, sabirnice):  # konstruktor
        super().__init__(prekidac, i_rastavljac, u_rastavljac, sabirnice) # konstruktor nad klase: Polje
        self.grupni_iskljucenje = StanjeOp.PRESTANAK           # klasa: StanjeOp (enum vrijednost) 
        self.grupni_upozorenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)  
        self.grupni_smetnje = StanjeOp.PRESTANAK               # klasa: StanjeOp (enum vrijednost)  

    def ukljuci(self):
        # Turn on the switch
        for rastavljac in self.s_rastavljaci:
                rastavljac.aktiviraj()
        
        self.prekidac.komanda(True)


    def iskljuci(self):
        # Turn off everything when switching is done
        self.prekidac.komanda(False)
        for rastavljač in self.s_rastavljaci:
            rastavljač.deaktiviraj()

