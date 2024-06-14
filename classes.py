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
        return isinstance(self.stanje, Stanje)
    

class Prekidac(PrimarnaOprema, ABC):
    def __init__(self):
        super().__init__()
    def dovoljnoSF6(self):
        return True
    def daljinskoUpravljanje(self):
        return True
    

class Rastavljac(PrimarnaOprema, ABC):
    def __init__(self, stanje=Stanje.UKLJUČEN):
        super().__init__(stanje)
        self.Prekidac = Prekidac()
    

class Zastita(ABC):
  
    def nije_u_proradi(self):
        # Get all attributes of the instance
        for attribute_name, attribute_value in self.__dict__.items():
            # Check if any attribute does not equal StanjeOp.PRESTANAK
            if attribute_value != StanjeOp.PRESTANAK:
                return False
        return True
    


class Polje(ABC):
    def __init__(self):
        random_bool = random.choice([True, False])
        if random_bool:
            self.prekidac = LTB145D1()
        else:
            self.prekidac = TPKoncar()
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
    def __init__(self):
        super().__init__()
     
              

class RIzlazni(Rastavljac):     # naslijeđuje klasu Rastavljac
    def __init__(self):
        super().__init__()                     #  nema svojih atributa

class RUzemljenja(Rastavljac):
    def __init__(self, state=Stanje.ISKLJUČEN):
        super().__init__(state)
        
    



class DalekovodnoPolje(Polje, ABC):                                  # naslijeđuje klasu Polje
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
    
#Upravljanje uređajima ovdje i za sabirničke rastavljače u posebnim dp za 1 i 2 sabirnice
    def ukljuci_prekidac(self):
        self.prekidac.komanda(True)
        print("Prekidac uključen, svi uredaji imaju napajanje")

    def iskljuci_prekidac(self):
        self.prekidac.komanda(False)
        print("Prekidac isključen, nema napajanja")

    def interakcija_prekidac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_prekidac()
        else:   
            self.ukljuci_prekidac()


    def ukljuci_i_rastavljac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. I rastavljač se ne može ", "uključiti." if self.i_rastavljac.odredi_polozaj() == Stanje.ISKLJUČEN else "isključiti.")
            return
        self.i_rastavljac.komanda(True)
        print("Izlazni rastavljac ukljucen")

    def iskljuci_i_rastavljac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. I rastavljač se ne može ", "uključiti." if self.i_rastavljac.odredi_polozaj() == Stanje.ISKLJUČEN else "isključiti.")
            return
        self.i_rastavljac.komanda(False)
        print("Izlazni rastavljac iskljucen")

    def interakcija_i_rastavljac(self):
        if self.i_rastavljac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_i_rastavljac()
        else:   
            self.ukljuci_i_rastavljac()


    def ukljuci_u_rastavljac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. U rastavljač se ne može ", "uključiti." if self.u_rastavljac.odredi_polozaj() == Stanje.ISKLJUČEN else "isključiti.")
            return
        self.u_rastavljac.komanda(True)
        print("Izlazni rastavljac ukljucen")

    def iskljuci_u_rastavljac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. U rastavljač se ne može ", "uključiti." if self.u_rastavljac.odredi_polozaj() == Stanje.ISKLJUČEN else "isključiti.")
            return
        self.u_rastavljac.komanda(False)
        print("Izlazni rastavljac iskljucen")

    def interakcija_u_rastavljac(self):
        if self.u_rastavljac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_u_rastavljac()
        else:   
            self.ukljuci_u_rastavljac()

    
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
    def __init__(self, num=2):
        super().__init__()

        self.aktivna_sabirnica=num
        self.s_rastavljacS1=RSabirnicki()
        self.s_rastavljacS2=RSabirnicki()
        match num:
            case 1:
                self.s_rastavljacS1.komanda(True)
                
            case 2:
                self.s_rastavljacS2.komanda(True)
        
        self.S_polje=SpojnoPolje()
        
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
        self.S_polje.iskljuci()
        print("Spojeno na S", num)

    def ukljuci_s_rastavljac(self, num):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. S_rastavljač se ne može uključiti.")
            return
        match num:
            case 1:
                self.s_rastavljacS1.komanda(True)
            case 2:
                self.s_rastavljacS2.komanda(True)
        print(f"S_rastavljac {num} ukljucen")

    def iskljuci_s_rastavljac(self, num):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. S_rastavljač se ne može isključiti.")
            return
        match num:
            case 1:
                self.s_rastavljacS1.komanda(False)
            case 2:
                self.s_rastavljacS2.komanda(False)
        print(f"S_rastavljac {num} iskljucen")
        
    def interakcija_s1_rastavljac(self):
        if self.s_rastavljacS1.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_s_rastavljac(1)
        else:   
            self.ukljuci_s_rastavljac(1)
    def interakcija_s2_rastavljac(self):
        if self.s_rastavljacS2.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_s_rastavljac(2)
        else:   
            self.ukljuci_s_rastavljac(2)

        
        
class Dalekovodno1Sab(DalekovodnoPolje):
    def __init__(self):
        super().__init__()

        self.s_rastavljac=RSabirnicki()
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
    
    def ukljuci_s_rastavljac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. S_rastavljač se ne može uključiti.")
            return
    
        self.s_rastavljac.komanda(True)
        print(f"S_rastavljac ukljucen")

    def iskljuci_s_rastavljac(self):
        if self.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
            print("Prekidac je uključen. S_rastavljač se ne može isključiti.")
            return
        self.s_rastavljac.komanda(False)
        print(f"S_rastavljac iskljucen")
        
    def interakcija_s_rastavljac(self):
        if self.s_rastavljac.odredi_polozaj() == Stanje.UKLJUČEN:
            self.iskljuci_s_rastavljac()
        else:   
            self.ukljuci_s_rastavljac()




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
    def __init__(self, num=2):
        self.D_polje1 = Dalekovodno1Sab()
        self.D_polje2 = Dalekovodno2Sab(num)
    
    
    def ukljuci(self, num):
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

class SpojnoPolje(Polje):                                      # naslijeđuje klasu Polje 
    def __init__(self, stanje=Stanje.ISKLJUČEN):  # konstruktor
        super().__init__() # konstruktor nad klase: Polje
        self.grupni_iskljucenje = StanjeOp.PRESTANAK           # klasa: StanjeOp (enum vrijednost) 
        self.grupni_upozorenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)  
        self.grupni_smetnje = StanjeOp.PRESTANAK               # klasa: StanjeOp (enum vrijednost)
        self.stanje=stanje
        self.s_rastavljacS1 = RSabirnicki()
        self.s_rastavljacS2 = RSabirnicki()

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