"skapa bräda, matris med varje lista en rad vars värden är kolonner,"

class Spelbräda:
    def __init__(self, matrisstorlek, symbol1="1", symbol2="2"):
        self.matrisstorlek = matrisstorlek
        self.spelbräda = self.skapa_matris_spelbräda()
        self.symbol1 = symbol1
        self.symbol2 = symbol2


    def skapa_matris_spelbräda(self):
        """Metod som skapar en kvadratisk matris med storleken specifierad i klassen Spelbräda
           med en struktur där 1:or är motståndarens spelpjäser, 2:or är spelarens spelpjäser
           och nollor är tomma rutor på brädan"""
        matris_spelbräda=[]
        for i in range(int(self.matrisstorlek)):
            i=i+1
            rad=[]
            if i==int(self.matrisstorlek)/2 or i==int(self.matrisstorlek)/2 + 1:
                noll_modell=[0]
                rad.extend(noll_modell*(int(self.matrisstorlek)))
                matris_spelbräda.append(rad)
                continue
            if i<int(self.matrisstorlek)/2:
                if i % 2 != 0:
                    ojämn_model=[0,1]
                    rad.extend(ojämn_model*(int(self.matrisstorlek/2)))
                else:
                    jämn_model=(1,0)
                    rad.extend(jämn_model*(int(self.matrisstorlek/2)))
            else:
                if i % 2 != 0:
                    ojämn_model=[0,2]
                    rad.extend(ojämn_model*(int(self.matrisstorlek/2)))
                else:
                    jämn_model=(2,0)
                    rad.extend(jämn_model*(int(self.matrisstorlek/2)))
            matris_spelbräda.append(rad)
        return matris_spelbräda

    def __str__(self):
        raden = "  "
        for counter in range(1, self.matrisstorlek+1):
            raden += str(counter) + " "
        for index, rad in enumerate (self.spelbräda, start=1):
            raden += "\n" + str(index)+ " " + (((" ".join(map(str, rad))).replace("1", self.symbol1)).replace("2", self.symbol2)).replace("0", "-") 
        return raden + "\n"

    def flytta_pjäs(self, vald_pjäs_koordinater, vald_plats_koordinater):
        """kanke kör denna som bara skapar en ny punkt med ett värde i matrisen och inte ändrar något gammal
            alltså input är bara en rad och en kolumn samt matris
            input:- output: matris """ 
        self.spelbräda[vald_plats_koordinater[0]][vald_plats_koordinater[1]] = self.spelbräda[vald_pjäs_koordinater[0]][vald_pjäs_koordinater[1]]
        self.spelbräda[vald_pjäs_koordinater[0]][vald_pjäs_koordinater[1]] = 0
        return self.spelbräda


class Spela(Spelbräda):

    def granskaspelplan(self):
        "kollar efter lagliga drag"


    def kolla_ifall_vald_pjäs_finns(self, vald_pjäs_koordinater):
        """ kollar ifall vald_pjäs anger en position på brädan där det antingen står 1 eller 2 alltså in 0
            input: lista av integers
            output: True eller False"""
        if self.spelbräda[vald_pjäs_koordinater[0]][vald_pjäs_koordinater[1]] == 0:
            return False
        else:
            return True

    def kolla_dragdiagonalitet(self, pjäs, plats):
        """ kollar så de valda draget är diagonalt
            input: två listor av integers
            outpt: True eller False""" "True diagonality, oavsett hur långt de är ifrån varandra"
        try:
            if abs(pjäs[0]-plats[0])/abs(pjäs[1]-plats[1]) != 1:
                return False
            else: 
                return True
        except:
            return False

    def kolla_ta_pjäs(self, pjäs, plats):
        attackerad_pjäs = list(map(sum,zip(pjäs,[1,1])))
        if 3 > abs(pjäs[0]-plats[0]) > 1 and self.kolla_ifall_vald_pjäs_finns(attackerad_pjäs) == True:
            return True
        else:
            return False

    def kolla_laglilg_sträcka_flytta(self, pjäs, plats):
        if 2 > abs(pjäs[0]-plats[0]) > 0:
            return True 
        else:
            return False


def bokstavskollen(bokstav):
    while True:
        try:
            bokstav=int(bokstav)
            break
        except ValueError:
            bokstav=input("Du måste skriva in ett heltal, försök igen: ")
            break        
    return str(bokstav)
        

def välj_pjäs():
        """funktion som frågar spelaren efter en ojäs och sparar koordinaterna i en lista som rad och kolonn
           output: lista av 2 integers"""
        vald_pjäs_koordinater = list(map(int,(bokstavskollen(input("Skriv position i ett nummer. Ex rad 2 och kolonn 4 blir 24: ")))))
        for i in range(len(vald_pjäs_koordinater)): vald_pjäs_koordinater[i] = vald_pjäs_koordinater[i]-1
        return vald_pjäs_koordinater

def välj_och_kolla_plats(typ_av_drag = 0):
    """ funtkion som ber användaren att välja en pjäs samt kollar så att det står en pjäs på den platsen
        input: string
        output: lista av två integers """
    while True:
        vald_pjäs_koordinater = välj_pjäs()
        pjäs_existerar = bräda.kolla_ifall_vald_pjäs_finns(vald_pjäs_koordinater)
        if pjäs_existerar == True and typ_av_drag == "välj": 
            break
        elif pjäs_existerar == False and typ_av_drag == "flytta":
            break
        elif pjäs_existerar == False and typ_av_drag == "välj":
            print("\nDet står ingen pjäs på den positionen ")
            continue
        elif pjäs_existerar == False and typ_av_drag == 0:
            break
        else:
            print("\nDet står redan en pjäs på platsen du valt")
            continue
    return vald_pjäs_koordinater

def kolla_dragdiagonalitet(pjäs, plats):
    """ Kollar diagonalitet i draget
        Input: två listor av integers
        Output: en lista av integers"""
    while True: 
        dragdiagonalitet = bräda.kolla_dragdiagonalitet(pjäs,plats)
        if dragdiagonalitet == True:
            break
        else:
            print("Pjäser kan bara röra sig diagonalt")
            plats = välj_och_kolla_plats()
    return plats

def kolla_ta_pjäs_eller_flytta(pjäs, plats):
    while True:
        ta_pjäs = bräda.kolla_ta_pjäs(pjäs, plats)
        laglig_sträcka = bräda.kolla_laglilg_sträcka_flytta(pjäs, plats)
        if ta_pjäs == True:
            break
        elif laglig_sträcka == True:
            break
        else:
            print("\nEn pjäs kan bara röra sig en ruta i taget om den inte hoppar över en motståndarpjäs: ")
            plats = välj_och_kolla_plats()
    return plats




def huvudprogram():
    print("\nVälkommen till damspelet")
    matrisstorlek = int(input("Hur stor bräda vill du ha? "))
    global bräda
    bräda = Spela(matrisstorlek)
    while True:
        print(bräda)
        for i in range(1,3):
            if i == 1:
                typ_av_drag = "välj"
                print("\nvälj en pjäs att flytta")
                vald_pjäs_koordinater = välj_och_kolla_plats(typ_av_drag)
            else: 
                typ_av_drag = "flytta"
                print("\nvälj en plats att flytta till")
                vald_plats_koordinater = kolla_ta_pjäs_eller_flytta(vald_pjäs_koordinater, kolla_dragdiagonalitet(vald_pjäs_koordinater, välj_och_kolla_plats(typ_av_drag)))
        bräda.flytta_pjäs(vald_pjäs_koordinater, vald_plats_koordinater)
    
    
""" bräda1=Spelbräda(8)
matris1=bräda1.skapa_matris_spelbräda()
print(matris1)
print(bräda1)
'bräda1.chomp(bräda1.skapa_matris_spelbräda(),3,2)'
'bräda1.print_matris(bräda1.chomp(bräda1.skapa_matris_spelbräda(),2,1))'
"bräda1.print_matris(bräda1.flytta_pjäs(matris1, 7, 4, 5, 3))"
spel1 = Spela(matris1) 
print(spel1.vald_pjäs)
print(spel1.slutgiltig_plats)
bräda1.spelbräda = spel1.flytta_pjäs()
matris2 = spel1.flytta_pjäs()
print(matris2)
print(bräda1) """
huvudprogram()