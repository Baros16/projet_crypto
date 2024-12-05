import random
import bibliotheque
import math
#definiissons une classe qui va nous permettre de stocker les mots francais pour une recherche rapide
class DictionnaireFrancais:
    def __init__(self, fichier):
        self.mots = set()
        self.charger_dictionnaire(fichier)

    def charger_dictionnaire(self, fichier):#lis un fichier et ajoute chaques mots a l'ensemble
        with open(fichier, 'r', encoding='utf-8') as f:
            for ligne in f:
                self.mots.add(ligne.strip().lower())

    def est_mot_francais(self, mot):#verifie si un mot est dans l'ensemble
        return mot.lower() in self.mots


def verification(matrice):
    if not matrice or len(matrice) == 0:
        return None  # Matrice vide ou invalide

    nb_lignes = len(matrice)
    nb_colonnes = len(matrice[0]) if nb_lignes > 0 else 0

    # Verification si la matrice est rectangulaire et suffisamment grande
    if nb_colonnes == 0 or any(len(ligne) != nb_colonnes for ligne in matrice):
        return None #Matrice non rectangulaire
    if nb_colonnes * nb_lignes < 9:
        return None  # Matrice trop petite


    mots = []
    index = 0
    for i in range(2, 11):  #On itere de 2 a 10 car on souhaite creer 9 mots
        mot = ""
        for ligne in matrice:
            for j in range(nb_colonnes):
                if index < i:
                    mot += ligne[j]
                    index += 1
                else:
                    break
            if index >= i:
                break
        mots.append(mot)
        index = 0 #On remet index a 0 pour le mot suivant
        #verifion si les premiers mots forme a partir de la matrice appartiennent a notre dictionnaire
    for t_mots in mots:
        if dictionnaire.est_mot_francais(t_mots):
            return True #on repere un mot francais dans les premieres phrases
    return False #aucun mot repere 
    

    


def force_brute(texte,n):

    print("debut de la boucle de test : veillez patienter . le programme teste les combinaisons")
    while True:
        cle_essaie = random.sample(range(n),n)
        if (len(texte)/n == 0):
            ligne = int(len(texte)/n + 1)
            reste = 0
        else :
            reste = len(texte) % n
            ligne = int(math.floor(len(texte)/n) + 1)
        proba = bibliotheque.decrypt_LVLUP(texte,cle_essaie,ligne,n,reste)
        if verification(proba):
            print("cette combinaison de mots peut etre probable")
            for i in range(ligne):
                for j in range(n):
                    if proba[i][j] is not None:
                        print(f"{proba[i][j]}",end="")
            print()
            print(f"la clef utilise est{cle_essaie}")
            tt = int(input("apuiyer sur '1' pour continuer ou '2'pour arreter la boucle de test"))
            if tt == 1:
                print("continuons la boucle de test")
                continue
            else:
                print("vous avez arrete la boucle de test")
                break
        elif not verification(proba) :
            continue
        else:
            print("message trop court . le programme ne saurais le traiter")
            break


                
def check(toto,tt):
    return tt in toto


def creer_ensemble(n):
    lig = math.factorial(n)
    ensmble = []
    i = 0
    while i < lig:
        tt = random.sample(range(n),n)
        if not check(ensmble,tt):
            ensmble.append(tt)
            i += 1
        else:
            continue
    return ensmble


def force_s_cle(texte):
    for n in range(3,8):
        trouve = False
        ENS = creer_ensemble(n)
        for element in ENS:
            if (len(texte) / n == 0):
                ligne = int(len(texte) / n + 1)
                reste = 0
            else:
                reste = len(texte) % n
                ligne = int(math.floor(len(texte) / n) + 1)
            proba = bibliotheque.decrypt_LVLUP(texte, element, ligne, n, reste)
            if verification(proba) :
                print("cette combinaison de mots peut etre probable")
                for i in range(ligne):
                    for j in range(n):
                        if proba[i][j] is not None:
                            print(f"{proba[i][j]}", end="")
                print()
                print(f"la clef utilise est{element}")
                tt = int(input("apuiyer sur '1' pour continuer ou '2'pour arreter la boucle de test"))
                if tt == 1:
                    print("continuons la boucle de test")
                    continue
                else:
                    print("felicitation vous avez arrete la boucle de test")
                    trouve = True
                    break
            elif not verification(proba):
                continue
            else:
                print("message trop court . le programme ne saurais le traiter")
                break
        if trouve == True:
            break

#debut du programme
if __name__ == "__main__":
    dictionnaire = DictionnaireFrancais('mots_francais.txt')
    vee_error = -1
    while(vee_error == -1):
        chaine_clai = input("veillez entrer le message a decoder")
        try:
            chaine_clai = str(chaine_clai)
        except ValueError:
            print("chaine de caractere invalide")
            continue
        vee_error = 1
    texte = bibliotheque.sup_speciaux(chaine_clai)
    ttt = int(input("conaissez vous la taille de la cle? si oui cliquez sur '1' sinon sur 2"))
    if ttt == 1:
        Taille = int(input("veillez entrer la taille de votre cle"))
        force_brute(texte,Taille)
    else:
        print("le programme seras plus complexe et nous allons faire des tests sur des clef allant de 3 a 10 caracteres")
        force_s_cle(texte)

        
