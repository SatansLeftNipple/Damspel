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
            "if sats som kollar ifall det är de två mittersta nollraderna"
            if i==int(self.matrisstorlek)/2 or i==int(self.matrisstorlek)/2 + 1:
                noll_modell=[0]
                rad.extend(noll_modell*(int(self.matrisstorlek)))
                matris_spelbräda.append(rad)
                continue
            "if sats som först kollar ifall det är övre/undre delen av spelplanen och sedan ifall det är en jämn eller udda rad"
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
        raden = "   "
        #lägger till den första raden som visar kolonners nummer
        for counter in range(1, self.matrisstorlek+1):
            raden += "{0:<3}".format(str(counter))
        # index räknas upp genom varje iteration och läggs till som det första numret till varje rad
        for index, rad in enumerate (self.spelbräda, start=1):
            raden += "\n" + "{0:<3s}".format(str(index)) + (((((("  ".join(map(str, rad))).replace("10", "W")).replace("20", "L")).replace("1", self.symbol1)).replace("2", self.symbol2)).replace("0", "-"))
        return raden + "\n"


    def flytta_pjäs(self, vald_pjäs_koordinater, vald_plats_koordinater):
        """kanke kör denna som bara skapar en ny punkt med ett värde i matrisen och inte ändrar något gammal
            alltså input är bara en rad och en kolumn samt matris
            input:- output: matris """ 
        self.spelbräda[vald_plats_koordinater[0]][vald_plats_koordinater[1]] = self.spelbräda[vald_pjäs_koordinater[0]][vald_pjäs_koordinater[1]]
        self.spelbräda[vald_pjäs_koordinater[0]][vald_pjäs_koordinater[1]] = 0

    def ta_pjäs(self, pjäs, plats, attackerad_pjäs):

        self.spelbräda[plats[0]][plats[1]] = self.spelbräda[pjäs[0]][pjäs[1]]
        self.spelbräda[pjäs[0]][pjäs[1]] = 0
        self.spelbräda[attackerad_pjäs[0]][attackerad_pjäs[1]] = 0
        #returnar pjäs för att den nya positionen skall kunna användas i kolla_obligatoriska_drag i huvudfunktionen igen
        return pjäs



class Spela(Spelbräda):

    def kolla_ifall_vald_pjäs_finns(self, pjäs, attackerad_pjäs=[0,0]):
        #kollar ifall vald_pjäs anger en position på brädan där det antingen står 1 eller 2 alltså in 0
        #input: lista av integers
        #output: True eller False"""
        #sparar värdena i någonting mer lätthanterligt
        pjäs_typ = self.spelbräda[pjäs[0]][pjäs[1]]
        attackerad_pjäs_typ = self.spelbräda[attackerad_pjäs[0]][attackerad_pjäs[1]]
        # if satsen kollar först om detta handlar om att kolla när en pjäs väljes eller när en pjäs attackeras, ifall == 0 är det ett val
        # sedan kollas ifall det står en pjäs, samt om pjäsen är av egen typ, måste även införa check för befodrade pjäser och vems tur det är
        if attackerad_pjäs == [0,0]:
            if pjäs_typ == 0:
                return False
            else:
                return True
        else:
            if attackerad_pjäs_typ != 0 and attackerad_pjäs_typ != pjäs_typ:
                return True 
            elif attackerad_pjäs_typ == pjäs_typ:
                print("\nDu kan inte attackera dina egna pjäser")
                return False    

    def kolla_dragdiagonalitet(self, pjäs, plats):
        #kollar så de valda draget är diagonalt
        #input: två listor av integers
        #outpt: True eller False""" "True diagonality, oavsett hur långt de är ifrån varandra
        try:
            if abs(pjäs[0]-plats[0])/abs(pjäs[1]-plats[1]) != 1:
                return False
            else: 
                return True
        except:
            return False

    def kolla_ta_pjäs(self, pjäs, plats):
        #Först kollas ifall pjäsen vald i matrisen är 1, 2 eller 3 för att se vilka platser funktionen skall kolla efter pjäser
        #där 3 är en befodrad pjäs sedan kollas så att platsen vald att gå till ligger på rätt avstånd
        #input: två listor av integers som båda innehåller två integers
        #output: False eller True
        #två if satser som bestämmer rad/kolonn skillnad mellan vald pjäs och attackerad pjäs
        if plats[0] > pjäs[0]:
            attackerad_pjäs = [1,0]
        elif plats[0] < pjäs[0]:
            attackerad_pjäs = [-1,0]

        if plats[1] > pjäs[1]:
            attackerad_pjäs[1] = 1
        elif plats[1] < pjäs[1]:
            attackerad_pjäs[1] = -1

        #summerar upp pjäs och rad/kolonn skillnad för de riktiga koordinaterna av attackerad_pjäs
        attackerad_pjäs = list(map(sum,zip(pjäs, attackerad_pjäs)))
            
        # if sats som kollar att avståndet på attacken bara är en pjäs samt att den pjäsen som attackeras finns och är laglig att attackera
        # error attackerar egna befodrade pjäser, detta kollas inte i funktionen
        if 3 > abs(pjäs[0]-plats[0]) > 1 and self.kolla_ifall_vald_pjäs_finns(pjäs, attackerad_pjäs) == True:
            return True, attackerad_pjäs
        else:
            return False, ""

    def kolla_laglilg_sträcka_flytta(self, pjäs, plats):
        if 2 > abs(pjäs[0]-plats[0]) > 0:
            return True 
        else:
            return False
    
    def kolla_laglig_rikting(self, pjäs, plats):
        #funktion kollar så att pjäser rör sig åt rätt håll
        typ_pjäs = self.spelbräda[pjäs[0]][pjäs[1]]
        if typ_pjäs == 1 and (pjäs[0] - plats[0]) > 0:
            return False
        elif typ_pjäs == 2 and (pjäs[0] - plats[0]) < 0:
            return False
        else:
            return True

    def kolla_vinst(self):
        spelare1 = 0
        spelare2 = 0
        for rad in self.spelbräda:
            for value in rad:
                if value == 1 or value == 10:
                    spelare1 += 1
                elif value == 2 or value == 20:
                    spelare2 += 1
        if spelare1 == 0 or spelare2 == 0:
            return True
        else:
            return False

        
    def kolla_obligatoriska_drag_höger_ner(self):
        # index1 tillhör rad och index2 tillhör kolonn
        for index1, a in enumerate (self.spelbräda):
            for index2, i in enumerate (a):
                #Try satsen ser till så att ifall index går över matrislängden så fortsätter funktionen vidare
                if index1+2 > self.matrisstorlek-1 or index2+2 > self.matrisstorlek-1 or i == 0 or i == 2:
                    continue
                höger_diagonal = self.spelbräda[index1+1][index2+1]
                # if satsen delar upp befordrade pjäser så att de inte multipliceras med 10, kanske gör en egen funktion för befordrade pjäser
                if i<10:
                    if höger_diagonal != 0 and höger_diagonal != i and höger_diagonal != i*10:
                        if self.spelbräda[index1+2][index2+2] == 0:
                            return True
                else:
                    if höger_diagonal != 0 and höger_diagonal != i and höger_diagonal != i/10:
                        if self.spelbräda[index1+2][index2+2] == 0:
                            return True

    def kolla_obligatoriska_drag_vänster_ner(self):
        for index1,a in enumerate (self.spelbräda):
            for index2, i in enumerate (a):
                # if satsen är för att index i listor kan bli mindre än noll och då räknar de istället upp ifrån höger sida
                if index1+2 > self.matrisstorlek-1  or index2-2 < 0 or i == 0 or i == 2: 
                    continue
                vänster_diagonal = self.spelbräda[index1+1][index2-1]
                #if sats delar upp befordrade pjäser
                if i<10:
                    if vänster_diagonal != 0 and vänster_diagonal != i and vänster_diagonal != i*10:
                        if self.spelbräda[index1+2][index2-2] == 0:
                            return True
                else:
                    if vänster_diagonal != 0 and vänster_diagonal != i and vänster_diagonal != i/10:
                        if self.spelbräda[index1+2][index2-2] == 0:
                            return True

    def kolla_obligatoriska_drag_höger_upp(self):
            # index1 tillhör rad och index2 tillhör kolonn
            for index1, a in enumerate (self.spelbräda[::-1]):
                for index2, i in enumerate (a):
                    #Try satsen ser till så att ifall index går över matrislängden så fortsätter funktionen vidare
                    if index1+2 > self.matrisstorlek-1 or index2+2 > self.matrisstorlek-1 or i == 0 or i == 1:
                        continue
                    höger_diagonal = self.spelbräda[::-1][index1+1][index2+1]
                    # if satsen delar upp befordrade pjäser så att de inte multipliceras med 10, kanske gör en egen funktion för befordrade pjäser
                    if i<10:
                        if höger_diagonal != 0 and höger_diagonal != i and höger_diagonal != i*10:
                            if self.spelbräda[::-1][index1+2][index2+2] == 0:
                                return True
                    else:
                        if höger_diagonal != 0 and höger_diagonal != i and höger_diagonal != i/10:
                            if self.spelbräda[::-1][index1+2][index2+2] == 0:
                                return True

    def kolla_obligatoriska_drag_vänster_upp(self):
        for index1,a in enumerate (self.spelbräda[::-1]):
            for index2, i in enumerate (a):
                # if satsen är för att index i listor kan bli mindre än noll och då räknar de istället upp ifrån höger sida
                if index1+2 > self.matrisstorlek-1  or index2-2 < 0 or i == 0 or i == 1: 
                    continue
                vänster_diagonal = self.spelbräda[::-1][index1+1][index2-1]
                #if sats delar upp befordrade pjäser
                if i<10:
                    if vänster_diagonal != 0 and vänster_diagonal != i and vänster_diagonal != i*10:
                        if self.spelbräda[::-1][index1+2][index2-2] == 0:
                            return True
                else:
                    if vänster_diagonal != 0 and vänster_diagonal != i and vänster_diagonal != i/10:
                        if self.spelbräda[::-1][index1+2][index2-2] == 0:
                            return True


def bokstavskollen(bokstav):
    while True:
        try:
            bokstav=int(bokstav)
            break
        except ValueError:
            bokstav=input("Du måste skriva in ett heltal, försök igen: ")
            break        
    return str(bokstav)
        
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

def kolla_vinst():
    pass

def obligatoriska_drag(pjäs):
    #input är ett värde antingen 1 eller 2 för att ange vilken spelares tur det är
    #output är bool värde
    typ_pjäs = bräda.spelbräda[pjäs[0]][pjäs[1]]
    if  typ_pjäs == 1 or typ_pjäs ==10:
        höger_ner = bräda.kolla_obligatoriska_drag_höger_ner()
        vänster_ner = bräda.kolla_obligatoriska_drag_vänster_ner()
        values = [höger_ner, vänster_ner]
        if typ_pjäs == 10:
            höger_upp = bräda.kolla_obligatoriska_drag_höger_upp()
            vänster_upp = bräda.kolla_obligatoriska_drag_vänster_upp()
            values.append((höger_upp, vänster_upp))

    elif typ_pjäs == 2 or typ_pjäs == 20:
        höger_upp = bräda.kolla_obligatoriska_drag_höger_upp()
        vänster_upp = bräda.kolla_obligatoriska_drag_vänster_upp()
        values = [höger_upp, vänster_upp]
        if typ_pjäs == 20:
            höger_ner = bräda.kolla_obligatoriska_drag_höger_ner()
            vänster_ner = bräda.kolla_obligatoriska_drag_vänster_ner()
            values.append((höger_ner, vänster_ner))
            
    if any(values) == True:
        return True
    else:
        return False

def välj_pjäser_spelare1():
    # Input: inget Output: tvp listor av integers
    # Ber spelare 1 att välja först en pjäs att flytta och sedan vart den skall flyttas
    while True:
        vald_pjäs = [int(a) for a in (input("Välj en pjäs. Skriv vilken rad, kolonn: ")).split(",")]
        # for satsen gör om koordinaterna till en mindre för att hamna på rätt plats i matrisen
        for i in range(len(vald_pjäs)): vald_pjäs[i] = vald_pjäs[i]-1
        typ_pjäs = bräda.spelbräda[vald_pjäs[0]][vald_pjäs[1]]
        #Typ_pjäs anger vilken typ av pjäs vald_pjäs är i matrisen, den säger sedan att du inte får välja att röra motståndarens pjäser
        if typ_pjäs == 2 or typ_pjäs == 20:
            print(f"\nDu kan bara välja pjäser av typ {bräda.symbol1}")
            continue    
        elif typ_pjäs == 0:
            print("\nDet står ingen pjäs här: ")
            continue
        # detta är en upprepning av koden innan för att välja filken position användaren vill plytta pjäsen till
        vald_plats = [int(a) for a in (input("Välj en plats. Skriv vilken rad, kolonn: ")).split(",")]
        for i in range(len(vald_plats)): vald_plats[i] = vald_plats[i]-1
        typ_plats = bräda.spelbräda[vald_plats[0]][vald_plats[1]]
        if typ_plats != 0:
            print("\nDet står en pjäs på denna plats redan")
            continue
        else:
            break
    return vald_pjäs, vald_plats


def välj_pjäser_spelare2():
    # Input: inget Output: två listor av integers
    # Ber spelare 2 att välja först en pjäs att flytta och sedan vart den skall flyttas
    while True:
        vald_pjäs = [int(a) for a in (input("Välj en  pjäs. Skriv vilken rad, kolonn: ")).split(",")]
        # for satsen gör om koordinaterna till en mindre för att hamna på rätt plats i matrisen
        for i in range(len(vald_pjäs)): vald_pjäs[i] = vald_pjäs[i]-1
        typ_pjäs = bräda.spelbräda[vald_pjäs[0]][vald_pjäs[1]]
        #Typ_pjäs anger vilken typ av pjäs vald_pjäs är i matrisen, den säger sedan att du inte får välja att röra motståndarens pjäser
        if typ_pjäs == 1 or typ_pjäs == 10:
            print(f"\nDu kan bara välja pjäser av typ {bräda.symbol2}")
            continue    
        elif typ_pjäs == 0:
            print("\nDet står ingen pjäs här: ")
            continue

        vald_plats = [int(a) for a in (input("Välj en plats. Skriv vilken rad, kolonn: ")).split(",")]
        for i in range(len(vald_plats)): vald_plats[i] = vald_plats[i]-1
        typ_plats = bräda.spelbräda[vald_plats[0]][vald_plats[1]]
        if typ_plats != 0:
            print("\nDet står en pjäs på denna plats redan")
            continue
        else:
            break
    return vald_pjäs, vald_plats

def utför_drag(pjäs, plats, attackerad_pjäs):
    #utför olika typer av drag beroende på input, typ ta_pjäs höger_upp, vänster_upp, höger_ner, vänster_ner, eller flytta
    if attackerad_pjäs == "":
        bräda.flytta_pjäs(pjäs, plats)
    else:
        # returnar ny_pjäs vilket är koordinaterna dit pjäsen befinner sig efter draget för att informationen måste användas i huvudfunktionen för att kolla_obligatoriska_drag
        ny_pjäs = bräda.ta_pjäs(pjäs, plats, attackerad_pjäs)
        return ny_pjäs

def befordra_pjäser():
    #går igenom spelplanen och befodrar pjäser
    for index, värde in enumerate (bräda.spelbräda[0]):
        if värde == 2:
            bräda.spelbräda[0][index] = 20
    for index, värde in enumerate (bräda.spelbräda[bräda.matrisstorlek - 1]):
        if värde == 1:
            bräda.spelbräda[bräda.matrisstorlek - 1][index] = 10

def huvudprogram():
    print("\nVälkommen till damspelet")
    matrisstorlek = int(input("Hur stor bräda vill du ha? "))
    symbol1 = input("välj symbol")
    symbol2 = input("välj symbol") 
    global bräda
    bräda = Spela(matrisstorlek, symbol1, symbol2)
    index = 0
    while True:
        index += 1
        befordra_pjäser()
        print(bräda)
        if index % 2 != 0:
            while True:
                pjäs, plats = välj_pjäser_spelare1()
                if kolla_dragdiagonalitet(pjäs, plats) == False: #i ordning, 
                    continue
                ta_pjäs, attackerad_pjäs = bräda.kolla_ta_pjäs(pjäs, plats)
                if obligatoriska_drag(pjäs) == True and ta_pjäs == True:
                    pass
                elif obligatoriska_drag(pjäs) == True and ta_pjäs == False:
                    print("\nDet finns obligatoriska drag att göra")
                    continue
                if ta_pjäs == False and bräda.kolla_laglilg_sträcka_flytta(pjäs, plats) == False:
                    print("\nså får du inte göra, din lilla råtta: ")
                    continue
                if bräda.kolla_laglig_rikting(pjäs, plats) == False:
                    print("\ndu kan inte röra dig i den riktningnen")
                    continue
                #måste kolla efter möjliga drag att ta pjäser, ifall det är True måste spelare ett göra ett till drag och därför plussas index med 1
                ny_pjäs = utför_drag(pjäs, plats, attackerad_pjäs)
                try:
                    if obligatoriska_drag(ny_pjäs) == True:
                        print("det finns obligatoriska drag att göra")
                        index += 1
                        continue
                except:
                    pass
                if bräda.kolla_vinst() == True:
                    break
                break
        else:
            while True:
                pjäs, plats = välj_pjäser_spelare2()
                if kolla_dragdiagonalitet(pjäs, plats) == False: #i ordning, 
                    continue
                ta_pjäs, attackerad_pjäs = bräda.kolla_ta_pjäs(pjäs, plats)
                if obligatoriska_drag(pjäs) == True and ta_pjäs == True:
                    pass
                elif obligatoriska_drag(pjäs) == True and ta_pjäs == False:
                    print("Det finns obligatoriska drag att göra")
                    continue
                if ta_pjäs == False and bräda.kolla_laglilg_sträcka_flytta(pjäs, plats) == False:
                    print("så får du inte göra, din lilla råtta: ")
                    continue
                ny_pjäs = utför_drag(pjäs, plats, attackerad_pjäs)
                try:
                    if obligatoriska_drag(ny_pjäs) == True:
                        print("det finns obligatoriska drag att göra")
                        index += 1
                        continue
                except:
                    pass
                if bräda.kolla_vinst() == True:
                    break
                break
        if bräda.kolla_vinst() == True:
            break
    print(bräda)
    print(f"grattis spelare {(index % 2)+1} har förlorat")
    
"""while True:
        befordra_pjäser()
        print(bräda)
        print(bräda.spelbräda)
        for i in range(1,3):
            if i == 1:
                typ_av_drag = "välj"
                print("\nvälj en pjäs att flytta")
                vald_pjäs_koordinater = välj_och_kolla_plats(typ_av_drag)
            else: 
                typ_av_drag = "flytta"
                print("\nvälj en plats att flytta till")
                while True:
                    vald_plats_koordinater = kolla_dragdiagonalitet(vald_pjäs_koordinater, välj_och_kolla_plats(typ_av_drag))
                    attack = bräda.kolla_ta_pjäs(vald_pjäs_koordinater, vald_plats_koordinater)
                    if attack == False:
                        break
                    else: 
                        _, attackerad_pjäs = bräda.kolla_ta_pjäs(vald_pjäs_koordinater, vald_plats_koordinater)
                        bräda.flytta_pjäs(attackerad_pjäs, attackerad_pjäs)
                        break

        bräda.flytta_pjäs(vald_pjäs_koordinater, vald_plats_koordinater)"""
    


"""while True:
        print(bräda)
        for i in range(1,3):
            if i == 1:
                typ_av_drag = "välj"
                print("\nvälj en pjäs att flytta")
                vald_pjäs_koordinater = välj_och_kolla_plats(typ_av_drag)
            else: 
                typ_av_drag = "flytta"
                print("\nvälj en plats att flytta till")
                vald_plats_koordinater = välj_och_kolla_plats(typ_av_drag)
                dragdiagonalitet = bräda.kolla_dragdiagonalitet(vald_pjäs_koordinater, vald_plats_koordinater)

                vald_plats_koordinater, attackerad_pjäs = kolla_ta_pjäs_eller_flytta(vald_pjäs_koordinater, dragdiagonalitet)
        bräda.flytta_pjäs(vald_pjäs_koordinater, vald_plats_koordinater) """
    
huvudprogram()