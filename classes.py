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


class PrimarnaOprema():
    def __init__(self, stanje):
        self.stanje = stanje

    def komanda(self, ukljuci): 
        self.stanje=ukljuci
        # return self.stanje     - mislim da je ovo suvišno, metoda odredi_polozaj vraća stanje, metoda komanda mijenja stanje
    
    def odredi_polozaj(self):
        return self.stanje
    

class Prekidac(PrimarnaOprema):
    pass

class Rastavljac(PrimarnaOprema):
    pass

class Zastita():           # uklonjeno naslijeđivanje da ne naslijeđuje Primarnu opremu prema klasnom dijagramu
    def __init__(self, stanje):
        self.stanje = stanje
    
    def odredi_stanje(self):
        return self.stanje      # dodan atribut stanje (tako da i Nadstrujna zaštita i distanttna zaštita imaju stanje)

class Polje():
    def __init__(self, prekidac, s_rastavljac, i_rastavljac):
        self.prekidac = prekidac
        self.s_rastavljac = s_rastavljac
        self.i_rastavljac = i_rastavljac


class PrekidacLTB145D1(Prekidac):                   # naslijeđuje klasu Prekidac
    def __init__(self, stanje):                     # konstruktor
        super().__init__(stanje)                    # konstruktor nad klase: Prekidac
        self.gubitak_sf6 = StanjeOp.PRESTANAK
        self.blokada_rada = StanjeOp.PRESTANAK
        self.blokada_isklopa = StanjeOp.PRESTANAK
        self.opruga_navijena = StanjeOp.PRESTANAK
    
    def provjeriGubitakSF6(self):
        return self.gubitak_sf6
    

class APU():
    def __init__(self):
        self.ukljucenje = StanjeOp.PRESTANAK
        self.p1 = StanjeOp.PRESTANAK
        self.p3 = StanjeOp.PRESTANAK
        self.blokada = StanjeOp.PRESTANAK

    def odredi_stanje(self):
        return # nisam siguran šta točno treba vratiti kao stanje apu-a
        
        
class Distantna(Zastita):
    def __init__(self, stanje):
        super().__init__(stanje)                    # konsruktor nad klase: Zastita
        self.iskljucenje = StanjeOp.PRESTANAK
        self.faza_l1 = StanjeOp.PRESTANAK
        self.faza_l2 = StanjeOp.PRESTANAK
        self.faza_l3 = StanjeOp.PRESTANAK
        self.zemljospoj = StanjeOp.PRESTANAK
        self.kvar = StanjeOp.PRESTANAK

class Nadstrujna(Zastita):
    def __init__(self, stanje):
        super().__init__(stanje)
        self.npc_iskljucenje = StanjeOp.PRESTANAK
        self.vpc_iskljucenje = StanjeOp.PRESTANAK
        self.zemljospojna_iskljucenje = StanjeOp.PRESTANAK
        self.od_preopterecenja_upozorenje = StanjeOp.PRESTANAK
        self.od_preopterecenja_iskljucenje = StanjeOp.PRESTANAK
        self.relej_kvar = StanjeOp.PRESTANAK

class MjerniPretvornik():
    def __init__(self, radna_energija, jalova_snaga):
        self.radna_energija = radna_energija
        self.jalova_snaga = jalova_snaga



class RSabirnicki(Rastavljac):  # naslijeđuje klasu Rastavljac
    pass                        #  nema svojih atributa

class RIzlazni(Rastavljac):     # naslijeđuje klasu Rastavljac
    pass                        #  nema svojih atributa


class DalekovodnoPolje(Polje):                                  # naslijeđuje klasu Polje
    def __init__(self, prekidac, s_rastavljac, i_rastavljac, dist_zastita, nads_zastita, apu, mjera, dalekovod): # konstruktor
        super().__init__(prekidac, s_rastavljac, i_rastavljac)  # konstruktor nad klase: Polje
        self.dist_zastita = dist_zastita                        # abstraktna: klasa Zastita/Distantna
        self.nads_zastita = nads_zastita                        # abstraktna: klasa Zastita/Nadstrujna
        self.apu = APU                                          # klasa: APU    
        self.mjera = mjera                                      # klasa: MjerniPretvornik
        self.grupni_iskljucenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)
        self.grupni_upozorenje = StanjeOp.PRESTANAK             # klasa: StanjeOp (enum vrijednost)
        self.grupni_smetnje = StanjeOp.PRESTANAK                # klasa: StanjeOp (enum vrijednost)
        self.dalekovod = dalekovod                              # + klasa: Dalekovod


class Napajanje():
    def __init__(self, stanje, kapacitet, napon, potrosnja):
        self.stanje = stanje
        self.kapacitet = kapacitet
        self.napon = napon
        self.potrosnja = potrosnja

    def odredi_stanje(self):
        return self.stanje

class TPKoncar(Prekidac):                           # naslijeđuje klasu Prekidac 
    def __init__(self, stanje, upravljanje, tlak):  # konstruktor
        super().__init__(stanje)                    # konstruktor nad klase: Prekidac
        self.tlak = tlak                            # ??
        self.pad_tlaka_16b = StanjeOp.PRESTANAK    
        self.pad_tlaka_14b = StanjeOp.PRESTANAK
        self.pad_tlaka_11b = StanjeOp.PRESTANAK
        self.apu_blokada = StanjeOp.PRESTANAK
        self.nesklad_polova_3p_isklop = StanjeOp.PRESTANAK
        self.upravljanje = upravljanje
    
    def odrediTlak(self):
        return self.tlak
    
    def odrediUpravljanje(self):
        return self.upravljanje

class Dalekovod():
    def ukljuci(self):
        print("Dalekovod uključen")

    def iskljuci(self):
        print("Dalekovod isključen")

class SpojnoPolje(Polje):                                      # naslijeđuje klasu Polje 
    def __init__(self, prekidac, s_rastavljac, i_rastavljac):  # konstruktor
        super().__init__(prekidac, s_rastavljac, i_rastavljac) # konstruktor nad klase: Polje
        self.grupni_iskljucenje = StanjeOp.PRESTANAK           # klasa: StanjeOp (enum vrijednost) 
        self.grupni_upozorenje = StanjeOp.PRESTANAK            # klasa: StanjeOp (enum vrijednost)  
        self.grupni_smetnje = StanjeOp.PRESTANAK               # klasa: StanjeOp (enum vrijednost)  
