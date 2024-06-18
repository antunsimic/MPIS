from enum import Enum
from abc import ABC
import random

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



def print_theRest(key, value, array):
    if value not in array:
        return
    for opposite in array:
        if value != opposite:
            print(key + " " + opposite)
            
def swap_s1_s2(word):
    if "S1" in word:
        return word.replace("S1", "S2")
    elif "S2" in word:
        return word.replace("S2", "S1")
    return word

class Napon:
    def __init__(self):
        self.powered = True

    def set_power(self, state):
        self.powered = state
        # print("Sustav napajanja je ", "uključen." if state else "isključen.")   Pošto se uključivanjem i isključivanjem prekidaća mjenja napajanje uređaja
                                                                                # mi to napajanje mjenjamo kroz for petlju za svaki uredaj pa da se ne ponavlja poruka
    def is_powered(self):
        return self.powered



class PrimarnaOprema(ABC):
    def __init__(self, polje, stanje=Stanje.UKLJUČEN):
        self.stanje = stanje
        self.napon=Napon() #ima napon
        self.polje = polje
    def komanda(self, ukljuci): 
        #ukljuci = true -> uključenje 
        #ukljuci = false -> isključenje
        if not self.ima_napajanje():
            print(f"{self.__class__.__name__} se ne može uključiti / isključiti, nema napajanja.")
            return None
        self.stanje= Stanje.UKLJUČEN if ukljuci else Stanje.ISKLJUČEN
        print(self.__class__.__name__, "uključen" if ukljuci else "isključen")
        return self.stanje
    
    def odredi_polozaj(self):
        return self.stanje
    
    def ima_napajanje(self):
        return self.napon.is_powered()
    
    def nije_nepoznato(self):
        return isinstance(self.stanje, Stanje)
    

class Prekidac(PrimarnaOprema, ABC):
    def __init__(self, polje):
        super().__init__(polje)
    def dovoljnoSF6(self):
        return True
    def daljinskoUpravljanje(self):
        return True
    

class Rastavljac(PrimarnaOprema, ABC):

    def __init__(self, polje, stanje=Stanje.UKLJUČEN):
        super().__init__(polje, stanje)


    

class Zastita(ABC):
    def __init__(self, polje):
        self.polje=polje
    def nije_u_proradi(self):
        # Get all attributes of the instance
        for attribute_name, attribute_value in self.__dict__.items():
            if attribute_name == 'polje':
                continue
            # Check if any attribute does not equal StanjeOp.PRESTANAK
            if attribute_value != StanjeOp.PRESTANAK:
                return False
        return True
    


class Polje(ABC):
    def __init__(self):
        random_bool = random.choice([True, False])
        if random_bool:
            self.prekidac = LTB145D1(self)
        else:
            self.prekidac = TPKoncar(self)
        self.i_rastavljac = RIzlazni(self)
        self.u_rastavljac = RUzemljenja(self)
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
    def ukljuci_prekidac(self):
        if not self.spreman_uredaj(self.prekidac):
            return
        if self.u_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Rastavljač uzemljenja nije isključen, stoga se prekidač ne može uključiti")
            return
        if self.s_rastavljacS2.odredi_polozaj() != Stanje.UKLJUČEN and self.s_rastavljacS1.odredi_polozaj() != Stanje.UKLJUČEN:
            print("Sabirnički rastavljač nije uključen, stoga se prekidač ne može uključiti")
            return
        if self.i_rastavljac.odredi_polozaj() != Stanje.UKLJUČEN:
            print("Linijski rastavljač nije uključen, stoga se prekidač ne može uključiti")
            return
        self.prekidac.komanda(True)
        
    def ukljuci_linijski_rastavljac(self):
        if not self.spreman_uredaj(self.i_rastavljac):
            return
        if self.u_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Rastavljač uzemljenja nije isključen, stoga se linijski rastavljač ne može uključiti")
            return

        self.i_rastavljac.komanda(True)
        
    def ukljuci_sabirnicki_rastavljac(self, num):
        if not self.spreman_uredaj(self.s_rastavljacS1) and num==1:
            return
        if not self.spreman_uredaj(self.s_rastavljacS2) and num==2:
            return
        
        if self.u_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Rastavljač uzemljenja nije isključen, stoga se sabirnički rastavljač ne može uključiti")
            return

        match num:
            case 1:
                self.s_rastavljacS1.komanda(True)
            case 2:
                self.s_rastavljacS2.komanda(True)
            case _:
                print("Nije nađen taj sabirnički rastavljač")
    
    def ukljuci_rastavljac_uzemljenja(self):
        if not self.spreman_uredaj(self.u_rastavljac):
            return
        if self.prekidac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Prekidač nije isključen, stoga se rastavljač za uzemljenje ne može uključiti")
            return
        if self.s_rastavljacS1.odredi_polozaj() != Stanje.ISKLJUČEN or self.s_rastavljacS2.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Jedan ili oba sabirnička rastavljača nisu isključena, stoga se rastavljač za uzemljenje ne može uključiti")
            return
        if self.i_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Linijski rastavljač nije isključen, stoga se rastavljač za uzemljenje ne može uključiti")
            return
        self.u_rastavljac.komanda(True)
    
    def iskljuci_prekidac(self):
        if not self.spreman_uredaj(self.prekidac):
            return
        self.prekidac.komanda(False)
        
    def iskljuci_linijski_rastavljac(self):
        if not self.spreman_uredaj(self.i_rastavljac):
            return
        if self.prekidac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Prekidač nije isključen, stoga se linijski rastavljač ne može isključiti")
            return
        self.i_rastavljac.komanda(False)
        
    def iskljuci_sabirnicki_rastavljac(self, num):
        if not self.spreman_uredaj(self.s_rastavljacS1) and num==1:
            return
        if not self.spreman_uredaj(self.s_rastavljacS2) and num==2:
            return
        if self.prekidac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Prekidač nije isključen, stoga se sabirnički rastavljač ne može isključiti")
            return


        match num:
            case 1:
                self.s_rastavljacS1.komanda(False)
            case 2:
                self.s_rastavljacS2.komanda(False)
            case _:
                print("Nije nađen taj sabirnički rastavljač")
    
    def iskljuci_rastavljac_uzemljenja(self):
        if not self.spreman_uredaj(self.u_rastavljac):
            return
        self.u_rastavljac.komanda(False)

    def interakcija_prekidac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_prekidac()
        else:   
            self.ukljuci_prekidac()

            
    def interakcija_i_rastavljac(self):
        if self.i_rastavljac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_linijski_rastavljac()
        else:   
            self.ukljuci_linijski_rastavljac()


    def interakcija_u_rastavljac(self):
        if self.u_rastavljac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_rastavljac_uzemljenja()
        else:   
            self.ukljuci_rastavljac_uzemljenja()
    def interakcija_s1_rastavljac(self):
        if self.s_rastavljacS1.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_sabirnicki_rastavljac(1)
        else:   
            self.ukljuci_sabirnicki_rastavljac(1)
    def interakcija_s2_rastavljac(self):
        if self.s_rastavljacS2.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_sabirnicki_rastavljac(2)
        else:   
            self.ukljuci_sabirnicki_rastavljac(2)


        match num:
            case 1:
                self.s_rastavljacS1.komanda(False)
            case 2:
                self.s_rastavljacS2.komanda(False)
            case _:
                print("Nije nađen taj sabirnički rastavljač")
    
    def iskljuci_rastavljac_uzemljenja(self):
        if not self.spreman_uredaj(self.u_rastavljac):
            return
        self.u_rastavljac.komanda(False)

        
    
class LTB145D1(Prekidac):                   # naslijeđuje klasu Prekidac
    def __init__(self, polje):                     # konstruktor
        super().__init__(polje)                    # konstruktor nad klase: Prekidac

        self.gubitak_sf6 = StanjeOp.PRESTANAK
        self.blokada_rada = StanjeOp.PRESTANAK
        self.blokada_isklopa = StanjeOp.PRESTANAK
        self.opruga_navijena = StanjeOp.PRESTANAK
    
    def dovoljnoSF6(self):
        return self.gubitak_sf6 == StanjeOp.PRESTANAK
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} prekidač komanda": "uklop" if self.stanje == Stanje.UKLJUČEN else "isklop",
            f"{self.polje.representation} prekidač stanje": self.stanje.value
        }
        # Add additional keys based on the current operational conditions
        state_info[f"{self.polje.representation} prekidač gubitak_SF6_upozorenje"] = self.gubitak_sf6.value
        state_info[f"{self.polje.representation} prekidač blokada_rada"] = self.blokada_rada.value
        state_info[f"{self.polje.representation} prekidač blokada_isklopa"] = self.blokada_isklopa.value
        state_info[f"{self.polje.representation} prekidač opruga_navijena_kvar"] = self.opruga_navijena.value
        
        return state_info


class APU(Zastita):
    def __init__(self, polje):
        super().__init__(polje)
        self.ukljucenje = StanjeOp.PRESTANAK
        self.p1 = StanjeOp.PRESTANAK
        self.p3 = StanjeOp.PRESTANAK
        self.blokada = StanjeOp.PRESTANAK
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} APU uključenje" : self.ukljucenje.value,
            f"{self.polje.representation} APU 1p" : self.p1.value,
            f"{self.polje.representation} APU 3p" : self.p3.value,
            f"{self.polje.representation} APU blokada" : self.blokada.value
        }
        # Add additional keys based on the current operational conditions
     
        return state_info


        
        
class Distantna(Zastita):
    def __init__(self, polje):
        super().__init__(polje)
        self.iskljucenje = StanjeOp.PRESTANAK
        self.faza_l1 = StanjeOp.PRESTANAK
        self.faza_l2 = StanjeOp.PRESTANAK
        self.faza_l3 = StanjeOp.PRESTANAK
        self.zemljospoj = StanjeOp.PRESTANAK
        self.kvar = StanjeOp.PRESTANAK
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} zaštita_distantna isključenje" : self.iskljucenje.value,
            f"{self.polje.representation} zaštita_distantna faza_L1_poticaj" : self.faza_l1.value,
            f"{self.polje.representation} zaštita_distantna faza_L2_poticaj" : self.faza_l2.value,
            f"{self.polje.representation} zaštita_distantna faza_L3_poticaj" : self.faza_l3.value,
            f"{self.polje.representation} zaštita_distantna zemljospoj_poticaj" : self.zemljospoj.value,
            f"{self.polje.representation} zaštita_distantna uređaj_kvar" : self.kvar.value   
        }
        # Add additional keys based on the current operational conditions
     
        return state_info

        

class Nadstrujna(Zastita):

    def __init__(self, polje):
        super().__init__(polje)
        self.npc_iskljucenje = StanjeOp.PRESTANAK
        self.vpc_iskljucenje = StanjeOp.PRESTANAK
        self.zemljospojna_iskljucenje = StanjeOp.PRESTANAK
        self.od_preopterecenja_upozorenje = StanjeOp.PRESTANAK
        self.od_preopterecenja_iskljucenje = StanjeOp.PRESTANAK
        self.relej_kvar = StanjeOp.PRESTANAK
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} zaštita_nadstrujna NPČ_isključenje" : self.npc_iskljucenje.value,
            f"{self.polje.representation} zaštita_nadstrujna VPČ_isključenje" : self.vpc_iskljucenje.value,
            f"{self.polje.representation} zaštita_nadstrujna zemljospojna_isključenje" : self.zemljospojna_iskljucenje.value,
            f"{self.polje.representation} zaštita_nadstrujna od_preopterećenja_upozorenje" : self.od_preopterecenja_upozorenje.value,
            f"{self.polje.representation} zaštita_nadstrujna od_preopterećenja_isključenje" : self.od_preopterecenja_iskljucenje.value,
            f"{self.polje.representation} zaštita_nadstrujna relej_kvar" : self.relej_kvar.value   
        }
        # Add additional keys based on the current operational conditions
     
        return state_info


class MjerniPretvornik:

    def __init__(self, polje, radna_energija=10, jalova_snaga=10):
        if not isinstance(radna_energija, (int, float)):
            raise ValueError("radna_energija must be a numerical value")
        if not isinstance(jalova_snaga, (int, float)):
            raise ValueError("jalova_snaga must be a numerical value")
        self.radna_energija = radna_energija
        self.jalova_snaga = jalova_snaga
        self.polje=polje
        
        
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} mjerni_pretvornik jalova_snaga_(MVAr)" : self.jalova_snaga,
            f"{self.polje.representation} brojilo radna_energija_(kWh)" : self.radna_energija, 
        }
        # Add additional keys based on the current operational conditions
     
        return state_info
       
        

class RSabirnicki(Rastavljac):  # naslijeđuje klasu Rastavljac
    def __init__(self, sabirnica, polje):
        super().__init__(polje)
        self.sabirnica = sabirnica
        
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} rastavljač_sabirnički_{self.sabirnica} komanda": "uklop" if self.stanje == Stanje.UKLJUČEN else "isklop",
            f"{self.polje.representation} rastavljač_sabirnički_{self.sabirnica} stanje": self.stanje.value
        }
     
        return state_info
     
              

class RIzlazni(Rastavljac):     # naslijeđuje klasu Rastavljac
    def __init__(self, polje):
        super().__init__(polje)
                     #  nema svojih atributa
                     
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} rastavljač_izlazni komanda": "uklop" if self.stanje == Stanje.UKLJUČEN else "isklop",
            f"{self.polje.representation} rastavljač_izlazni stanje": self.stanje.value
        }
     
        return state_info

class RUzemljenja(Rastavljac):
    def __init__(self, polje, state=Stanje.ISKLJUČEN):
        super().__init__(polje, state)

    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
           # "rastavljač_uzemljenja komanda": "uklop" if self.stanje == Stanje.UKLJUČEN else "isklop",
            f"{self.polje.representation} rastavljač_uzemljenja stanje": self.stanje.value
        }
     
        return state_info
    



class DalekovodnoPolje(Polje, ABC):                                  # naslijeđuje klasu Polje
    def __init__(self): # konstruktor
        super().__init__()  # konstruktor nad klase: Polje
   
        self.dist_zastita = Distantna(self)
        self.nads_zastita = Nadstrujna(self)                        # abstraktna: klasa Zastita/Nadstrujna
        self.apu = APU(self)                                          # klasa: APU    
        self.mjera = MjerniPretvornik(self)                                      # klasa: MjerniPretvornik
        self.grupni_iskljucenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)
        self.grupni_upozorenje = StanjeOp.PRESTANAK             # klasa: StanjeOp (enum vrijednost)
        self.grupni_smetnje = StanjeOp.PRESTANAK                # klasa: StanjeOp (enum vrijednost)

    def zastita_nije_u_proradi(self):
        for zastita in [self.dist_zastita, self.nads_zastita, self.apu]:
            if not zastita.nije_u_proradi():
                print(f"{zastita.__class__.__name__} je u proradi.")
                self.prekidac.komanda(False)
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
    
    def spreman_uredaj(self, uredaj):
        if not self.zastita_nije_u_proradi():
            print("Zašita je u proradi. Uređaj se ne može uključiti / isključiti.")
            return False
        if not uredaj.ima_napajanje():
            print("Uređaj nema napajanje. Stoga se ne može uključiti / isključiti")
            return False
        if isinstance(uredaj, Prekidac) and not uredaj.dovoljnoSF6():
            print("Razina plina SF6 je preniska. Prekidač se ne može uključiti / isključiti")
            return False
        if isinstance(uredaj, Prekidac) and not uredaj.daljinskoUpravljanje():
            print("Daljinsko upravljanje nije omogućeno. Prekidač se ne može uključiti / isključiti")
            return False
        if not uredaj.nije_nepoznato():
            print("Stanje uređaja je nepoznato. Potrebno je poslati osoblje u rasklopno postrojenje. Uređaj se ne može uključiti / isključiti")
            return False
        return True

class Dalekovodno2Sab(DalekovodnoPolje):
    def __init__(self, num=2):
        super().__init__()
        self.representation = "TS_D1_110kV DV_D1_S" + str(num)
        self.aktivna_sabirnica=num
        self.s_rastavljacS1=RSabirnicki(1, self)
        self.s_rastavljacS2=RSabirnicki(2, self)
        match num:
            case 1:
                self.s_rastavljacS1.komanda(True)
                self.s_rastavljacS2.komanda(False)
                
            case 2:
                self.s_rastavljacS2.komanda(True)
                self.s_rastavljacS1.komanda(False)
        
        self.S_polje=SpojnoPolje()
        self.S_polje.iskljuci()
        
    def prespoji(self, num):
        # Control the SpojnoPolje to switch to the new busbar
        if not self.S_polje.spremno():
            print("Spojno polje nije spremno")
            print("Prespajanje neuspješno")
            return
        self.S_polje.ukljuci()
        
        #prespajanje
        match num:
            case 1:
                self.s_rastavljacS1.komanda(True)
                self.s_rastavljacS2.komanda(False)
            case 2:
                self.s_rastavljacS2.komanda(True)
                self.s_rastavljacS1.komanda(False)
        self.aktivna_sabirnica = num
        self.representation = "TS_D1_110kV DV_D1_S" + str(num)
        self.S_polje.iskljuci()
        print("Spojeno na S", num)
        



        
class Dalekovodno1Sab(DalekovodnoPolje):
    def __init__(self):
        super().__init__()
        self.representation = "TS_D2_110kV DV_D2"
        self.s_rastavljac=RSabirnicki(1, self)
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
    
    def ukljuci_prekidac(self):
        if self.u_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Rastavljač uzemljenja nije isključen, stoga se prekidač ne može uključiti")
            return
        if self.s_rastavljac.odredi_polozaj() != Stanje.UKLJUČEN:
            print("Sabirnički rastavljač nije uključen, stoga se prekidač ne može uključiti")
            return
        if self.i_rastavljac.odredi_polozaj() != Stanje.UKLJUČEN:
            print("Linijski rastavljač nije uključen, stoga se prekidač ne može uključiti")
            return
        self.prekidac.komanda(True)
        
        
    def ukljuci_sabirnicki_rastavljac(self):
        if self.u_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Rastavljač uzemljenja nije isključen, stoga se prekidač ne može uključiti")
            return

        self.s_rastavljac.komanda(True)


    
    def ukljuci_rastavljac_uzemljenja(self):
        if self.prekidac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Prekidač nije isključen, stoga se rastavljač za uzemljenje ne može uključiti")
            return
        if self.s_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Sabirnički rastavljač nije isključen, stoga se rastavljač za uzemljenje ne može uključiti")
            return
        if self.i_rastavljac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Linijski rastavljač nije isključen, stoga se rastavljač za uzemljenje ne može uključiti")
            return
        self.u_rastavljac.komanda(True)
    
        
        
    def iskljuci_sabirnicki_rastavljac(self):
        if self.prekidac.odredi_polozaj() != Stanje.ISKLJUČEN:
            print("Prekidač nije isključen, stoga se sabirnički rastavljač ne može isključiti")
            return

        self.s_rastavljac.komanda(False)


    def interakcija_s_rastavljac(self):
        if self.s_rastavljac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_sabirnicki_rastavljac()
        else:   
            self.ukljuci_sabirnicki_rastavljac()

    
    




class TPKoncar(Prekidac):                           # naslijeđuje klasu Prekidac 
    def __init__(self, polje):  # konstruktor
        super().__init__(polje)                    # konstruktor nad klase: Prekidac
        
        self.pad_tlaka_16b = StanjeOp.PRESTANAK    

        self.pad_tlaka_14b = StanjeOp.PRESTANAK
        self.pad_tlaka_11b = StanjeOp.PRESTANAK
        self.apu_blokada = StanjeOp.PRESTANAK
        self.nesklad_polova_3p_isklop = StanjeOp.PRESTANAK
        self.upravljanje = Upravljanje.DALJINSKO
    
    
    def daljinskoUpravljanje(self):
        return self.upravljanje == Upravljanje.DALJINSKO
    def get_state_info(self):
        # Create a dictionary to store the state information
        state_info = {
            f"{self.polje.representation} prekidač komanda": "uklop" if self.stanje == Stanje.UKLJUČEN else "isklop",
            f"{self.polje.representation} prekidač stanje": self.stanje.value
        }
        # Add additional keys based on the current operational conditions
        state_info[f"{self.polje.representation} prekidač pad_tlaka<16b"] = self.pad_tlaka_16b.value
        state_info[f"{self.polje.representation} prekidač pad_tlaka<14b"] = self.pad_tlaka_14b.value
        state_info[f"{self.polje.representation} prekidač pad_tlaka<11b"] = self.pad_tlaka_11b.value
        state_info[f"{self.polje.representation} prekidač APU_blokada"] = self.apu_blokada.value
        state_info[f"{self.polje.representation} prekidač nesklad_polova_3P_isklop"] = self.nesklad_polova_3p_isklop.value
        state_info[f"{self.polje.representation} prekidač upravljanje"] = self.upravljanje.value        
        return state_info

        


class Dalekovod:
    def __init__(self, num=2):
        self.D_polje1 = Dalekovodno1Sab()
        self.D_polje2 = Dalekovodno2Sab(num)
    
    
    def ukljuci(self, num=2):
        for polje in [self.D_polje1, self.D_polje2]:
            if not polje.spremno():
                print("Stoga se dalekovod ne može uključiti.")
                return
        self.D_polje1.u_rastavljac.komanda(False)
        self.D_polje2.u_rastavljac.komanda(False)

        #uključiti sabirničke rastavljače s obje strane
        self.D_polje1.s_rastavljac.komanda(True)
        match num:
            case 1:
                self.D_polje2.s_rastavljacS1.komanda(True)
            case 2:
                self.D_polje2.s_rastavljacS2.komanda(True)
        self.D_polje2.aktivna_sabirnica=num
        #uključiti linijske rastavljače s obje strane
        self.D_polje1.i_rastavljac.komanda(True)
        self.D_polje2.i_rastavljac.komanda(True)
        #uključiti prekidače s obje strane
        self.D_polje1.prekidac.komanda(True)
        self.D_polje2.prekidac.komanda(True)
        
        print("Dalekovod uključen")

    def iskljuci(self):
        for polje in [self.D_polje1, self.D_polje2]:
            if not polje.spremno():
                print("Stoga se dalekovod ne može isključiti.")
                return
        #isključiti prekidače s obje strane
        self.D_polje1.prekidac.komanda(False)
        self.D_polje2.prekidac.komanda(False)
       
        #isključiti linijske rastavljače s obje strane
        self.D_polje1.i_rastavljac.komanda(False)
        self.D_polje2.i_rastavljac.komanda(False)
        
        #uključiti sabirničke rastavljače s obje strane
        self.D_polje1.s_rastavljac.komanda(False)
        self.D_polje2.s_rastavljacS1.komanda(False)
        self.D_polje2.s_rastavljacS2.komanda(False)
        
        #uključiti rastavljače za uzemljenje s obje strane
        self.D_polje1.u_rastavljac.komanda(True)
        self.D_polje2.u_rastavljac.komanda(True)
        
            
        print("Dalekovod isključen")
    
    def izlistaj(self, odabir="trenutne"):
        self.izlistaj_polje(self.D_polje1, odabir)
        self.izlistaj_polje(self.D_polje2, odabir)
        self.izlistaj_polje(self.D_polje2.S_polje, odabir)
       
        
    
    def izlistaj_polje(self, polje, odabir="trenutne"):
        if not isinstance(polje, Polje):
            print("Greška: metoda izlistaj_polje može se pozvati samo nad poljem")
            return
        # Iterate over all attributes of the object
        for attribute_name in dir(polje):
            uredaj = getattr(polje, attribute_name)
            # Check if the attribute is an object and has the 'get_state_info' method
            if hasattr(uredaj, 'get_state_info'):
                self.izlistaj_uredaj(uredaj, odabir)

    def izlistaj_uredaj(self, uredaj, odabir="trenutne"):
        if not hasattr(uredaj, "get_state_info"):
            print("Greška: metoda izlistaj_uredaj može se pozvati samo nad uređajima")
            return
        uredaj_signali = uredaj.get_state_info()
        for key, value in uredaj_signali.items():
            value=str(value)
            print(key + " " + value)
            if odabir=="sve":
                key2 = swap_s1_s2(key)
                if key2 != key: print(key2 + " " + value)
                stanje_values = [e.value for e in Stanje]
                stanjeop_values = [e.value for e in StanjeOp]
                upravljanje_values = [e.value for e in Upravljanje]
                if value in stanje_values:
                    print_theRest(key, value, stanje_values)
                    if key != key2: print_theRest(key2, value, stanje_values)
                elif value in stanjeop_values:
                    print_theRest(key, value, stanjeop_values)
                    if key != key2: print_theRest(key2, value, stanjeop_values)
                elif value in upravljanje_values:
                    print_theRest(key, value, upravljanje_values)
                    if key != key2: print_theRest(key2, value, upravljanje_values)


class SpojnoPolje(Polje):                                      # naslijeđuje klasu Polje 
    def __init__(self, stanje=Stanje.ISKLJUČEN):  # konstruktor
        super().__init__() # konstruktor nad klase: Polje
        self.grupni_iskljucenje = StanjeOp.PRESTANAK           # klasa: StanjeOp (enum vrijednost) 
        self.grupni_upozorenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)  
        self.grupni_smetnje = StanjeOp.PRESTANAK               # klasa: StanjeOp (enum vrijednost)
        self.stanje=stanje
        self.s_rastavljacS1 = RSabirnicki(1, self)
        self.s_rastavljacS2 = RSabirnicki(2, self)
        self.representation = "TS_D1_110kV SP_D1"

    def ukljuci(self):
        # Turn on the switch
        self.s_rastavljacS1.komanda(True)
        self.s_rastavljacS2.komanda(True)
        self.prekidac.komanda(True)


    def iskljuci(self):
        # Turn off everything when switching is done
        self.prekidac.komanda(False)
        self.s_rastavljacS1.komanda(False)
        self.s_rastavljacS2.komanda(False)  
    
            
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
    
    def spreman_uredaj(self, uredaj):
        if not uredaj.ima_napajanje():
            print("Uređaj nema napajanje. Stoga se ne može uključiti / isključiti")
            return False
        if isinstance(uredaj, Prekidac) and not uredaj.dovoljnoSF6():
            print("Razina plina SF6 je preniska. Prekidač se ne može uključiti / isključiti")
            return False
        if isinstance(uredaj, Prekidac) and not uredaj.daljinskoUpravljanje():
            print("Daljinsko upravljanje nije omogućeno. Prekidač se ne može uključiti / isključiti")
            return False
        if not uredaj.nije_nepoznato():
            print("Stanje uređaja je nepoznato. Potrebno je poslati osoblje u rasklopno postrojenje. Uređaj se ne može uključiti / isključiti")
            return False
        return True

    
class Line:
    def __init__(self, x0, y0, x1, y1, dalekovod, width):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.dalekovod = dalekovod

    def draw(self, canvas):
        canvas.create_line(self.x0, self.y0, self.x1, self.y1, width=self.width)

