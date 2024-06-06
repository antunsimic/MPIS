
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


class PrimarnaOprema:
    def __init__(self, stanje):
        self.stanje = stanje

    def komanda(self, ukljuci):
        pass

class Prekidac(PrimarnaOprema):
    pass

class Rastavljac(PrimarnaOprema):
    pass

class Zastita(PrimarnaOprema):
    pass

class Polje:
    def __init__(self, prekidac, s_rastavljac, i_rastavljac):
        self.prekidac = prekidac
        self.s_rastavljac = s_rastavljac
        self.i_rastavljac = i_rastavljac


class PrekidacLTB145D1(Prekidac):
    def __init__(self, stanje, gubitak_sf6, blokada_rada, blokada_isklopa, opruga_navijena):
        super().__init__(stanje)
        self.gubitak_sf6 = gubitak_sf6
        self.blokada_rada = blokada_rada
        self.blokada_isklopa = blokada_isklopa
        self.opruga_navijena = opruga_navijena

class APU():
    def __init__(self, ukljucenje, p1, p3, blokada):
        self.ukljucenje = ukljucenje
        self.p1 = p1
        self.p3 = p3
        self.blokada = blokada

class Distantna(Zastita):
    def __init__(self, iskljucenje, faza_l1, faza_l2, faza_l3, zemljospoj, kvar):
        self.iskljucenje = iskljucenje
        self.faza_l1 = faza_l1
        self.faza_l2 = faza_l2
        self.faza_l3 = faza_l3
        self.zemljospoj = zemljospoj
        self.kvar = kvar

class Nadstrujna(Zastita):
    def __init__(self, npc_iskljucenje, vpc_iskljucenje, zemljospojna_iskljucenje, od_preopterecenja_upozorenje, od_preopterecenja_iskljucenje, relej_kvar):
        self.npc_iskljucenje = npc_iskljucenje
        self.vpc_iskljucenje = vpc_iskljucenje
        self.zemljospojna_iskljucenje = zemljospojna_iskljucenje
        self.od_preopterecenja_upozorenje = od_preopterecenja_upozorenje
        self.od_preopterecenja_iskljucenje = od_preopterecenja_iskljucenje
        self.relej_kvar = relej_kvar

class MjerniPretvornik:
    def __init__(self, radna_energija, jalova_snaga):
        self.radna_energija = radna_energija
        self.jalova_snaga = jalova_snaga





class RSabirnicki(Rastavljac):
    pass  

class RIzlazni(Rastavljac):
    pass  

class DalekovodnoPolje(Polje):
    def __init__(self, prekidac, s_rastavljac, i_rastavljac, dist_zastita, nads_zastita, apu, mjera):
        super().__init__(prekidac, s_rastavljac, i_rastavljac)
        self.dist_zastita = dist_zastita
        self.nads_zastita = nads_zastita
        self.apu = apu
        self.mjera = mjera
        self.grupni_iskljucenje = StanjeOp.PRESTANAK  
        self.grupni_upozorenje = StanjeOp.PRORADA
        self.grupni_smetnje = StanjeOp.PRORADA

class Napajanje:
    def __init__(self, stanje, kapacitet, napon, potrosnja):
        self.stanje = stanje
        self.kapacitet = kapacitet
        self.napon = napon
        self.potrosnja = potrosnja

class TPKoncar(Rastavljac):
    def __init__(self):
        self.pad_tlaka_16b = StanjeOp.PRORADA
        self.pad_tlaka_14b = StanjeOp.PRORADA
        self.pad_tlaka_11b = StanjeOp.PRORADA
        self.apu_blokada = StanjeOp.PRORADA
        self.nesklad_polova_3p_isklop = StanjeOp.PRORADA
        self.upravljanje = Upravljanje.DALJINSKO

class Dalekovod:
    def ukljuci(self):
        print("Dalekovod uključen")

    def iskljuci(self):
        print("Dalekovod isključen")

class SpojnoPolje(Polje):
    def __init__(self, prekidac, s_rastavljac, i_rastavljac):
        super().__init__(prekidac, s_rastavljac, i_rastavljac)
        self.grupni_iskljucenje = StanjeOp.PRESTANAK
        self.grupni_upozorenje = StanjeOp.PRORADA
        self.grupni_smetnje = StanjeOp.PRORADA

