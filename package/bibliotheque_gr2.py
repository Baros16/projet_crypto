import re
import math
# 1 fonction pour extraire les indices des caracteres de la cle
def key_index(cleff):
    tuples_trie =sorted(enumerate(cleff),key=lambda x: x[1]) #craie une liste de tuples(caractes , indices)
    indice_trie = [indice for indice , _ in tuples_trie] #permet de extraire les indices
    return indice_trie



#   fontion pour supprimer les espaces dans le message

def sup_speciaux(chaine):
    chaine_saine = re.sub(r'[\s\'",.]', '', chaine)  # suprimme les espaces et caracteres speciaux
    nouv_list = list(chaine_saine)
    return nouv_list




# 5 fonction permettant de verifier si une cle ne contient pas de caracteres speciaux


def verifier(chainee):
    for caracteres in chainee:
        if not (caracteres.isalnum() or caracteres == '_'):
            return True  # caractere special trouve
    return False


#  fonction permettant de classer notre mot claire dans un tableau. elle prend en parametre les dimensions du tableau(ligne.colones)
def creer_tableau(liste_caracts,lignes,colones):
    if len(liste_caracts) != lignes * colones: #taille matrice incompatible
        A = lignes * colones - len(liste_caracts)
        caracteres_speciaux = ["*"]*A # cree une liste de caracteres speciaux 
        liste_fusionne = liste_caracts + [speciaux for speciaux in caracteres_speciaux] # ajoute la liste de caractes speciaux a l'ancienne liste
    else:
        liste_fusionne = liste_caracts
     # la taille de la matrice est donc conpatible
    tableau = [[None for _ in range(colones)]for _ in range(lignes)]
    #remplir le tableau
    index = 0
    for i in range(lignes):
        for j in range(colones):
            tableau[i][j] = liste_fusionne[index]
            index += 1
    return tableau


# elle permet de chiffrer
def reoganiser_colones(matrice,list_entier):
    if not matrice or not list_entier:
        return None
    nb_lignes = len(matrice)
    lambdaa = [[None for _ in range(len(list_entier))] for _ in range(nb_lignes)]
    for i in range(nb_lignes):
        for j, indice_colones in enumerate(list_entier):
            lambdaa[i][j] = matrice[i][indice_colones]
    return lambdaa


#fonction pour creer le txte final
def text_a_afficher(toto):
    # Verifie si la liste est vide
    if not toto or not isinstance(toto[0], list):
        return []

    # Initialiser une liste pour stocker les valeurs des colonnes
    txt_final = []

    # Nombre de colonnes
    nb_colonnes = len(toto[0])

    # Parcourir chaque colonne
    for col in range(nb_colonnes):
        for ligne in range(len(toto)):
            txt_final.append(toto[ligne][col])

    return txt_final

#permet de decrypter
def decrypt_LVLUP(texte,list,lignes,colones,reste):
    matrice = [[None for _ in range(colones)]for _ in range(lignes)]
    index = 0
    for col in range(colones):
        for i in range(len(list)):
            if col == list[i]:
                a = i
                break
        if a < reste:
            for lig in range(lignes):
                matrice[lig][a] = texte[index]
                index += 1
        else:
            for lig in range(lignes - 1):

                matrice[lig][a] = texte[index]
                index += 1
    return matrice


#index pour decrypter
def index_key(clef):
    # A - Classer les caracteres par ordre alphabetique et obtenir les indices
    toto = sorted(clef)
    
    # B - Creer un dictionnaire pour stocker les indices des caracteres
    indices_dict = {}
    for index, caractere in enumerate(toto):
        if caractere not in indices_dict:
            indices_dict[caractere] = []
        indices_dict[caractere].append(index)
    
    # C - Creer la liste des indices correspondant aux caracteres de clef
    indices = []
    for caractere in clef:
        indices.append(indices_dict[caractere].pop(0))  # Recuperer l'indice et le supprimer de la liste
    
    return indices

def decrypter_message(txt,cle):
    texte = txt.upper()
    texte_chif = sup_speciaux(texte)
    colones = len(cle)
    cle_indice = index_key(cle)
    mat = []
    if (len(texte_chif)/colones == 0):
        lignes = int(len(texte_chif)/colones + 1)
        reste = 0
        matrice_decryp = decrypt_LVLUP(texte_chif,cle_indice,lignes,colones,reste)
        for i in range(lignes):
            for j in range(colones):
               mat.append(matrice_decryp[i][j])
    else:
        reste = len(texte_chif) % colones
        ligne = int(math.floor(len(texte_chif)/colones) + 1)
        matrice_ch = decrypt_LVLUP(texte_chif,cle_indice,ligne,colones,reste)
        for i in range(ligne):
            for j in range(colones):
                if matrice_ch[i][j] is not None:
                    mat.append(matrice_ch[i][j])
    return ''.join(mat)

# fonction permettant de crypter
def crypter_message(texte, clef):
    cle = clef.upper()
    txt = texte.upper()
    cle_classe = key_index(cle)
    texte_en_claire = sup_speciaux(txt)
    colone = len(cle)
    if len(texte_en_claire) % colone == 0:
        ligne = int(len(texte_en_claire) / colone)
    else:
        ligne = int(math.floor(len(texte_en_claire) / colone) + 1)

    matrice = creer_tableau(texte_en_claire, ligne, colone)  # on crait notre matrice classe en ordre
    matrice_chifre = reoganiser_colones(matrice, cle_classe)
    texte_chifre = text_a_afficher(matrice_chifre)
    result_f = []
    for d in texte_chifre:
        if d != "*":
            result_f.append(d)
    resul = ''.join(result_f)
    return resul
