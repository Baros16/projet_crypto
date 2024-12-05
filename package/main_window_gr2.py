import io
import sys
from PySide6.QtWidgets import (QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QMessageBox, QTextEdit, QTextBrowser, QInputDialog)
import bibliotheque
import random
import math
import io


class Stream_To_Textedit(io.StringIO):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def write(self, message):
        self.text_edit.append(message)
        QApplication.processEvents()


class ChildWindow1(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setup_ui()
        self.setMinimumSize(400, 400)
        self.setStyleSheet("font-size: 18px;")
        self.te_edit.setPlaceholderText(text)

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widget_to_layout()
        self.setup_connections()

    def create_widgets(self):
        self.lbl_1 = QLabel(" Entrer la cle :")
        self.lbl_2 = QLabel(" Enter le message: ")
        self.le = QLineEdit()
        self.te_edit = QTextEdit()
        self.result = QTextBrowser()
        self.btn_start = QPushButton(" Start")
        self.btn_start.setStyleSheet("background-color: green; margin: 30px;")
        self.btn_clear = QPushButton(" Clear")
        self.btn_clear.setStyleSheet("background-color: grey; margin: 30px;")

    def create_layouts(self):
        self.layout = QVBoxLayout(self)
        self.middle_layout = QHBoxLayout()

    def modify_widgets(self):
        self.le.setPlaceholderText("Entre la cle")
        self.result.setHtml(" Le resultat s'affiche ici")

    def add_widget_to_layout(self):
        self.layout.addWidget(self.lbl_1)
        self.layout.addWidget(self.le)
        self.layout.addWidget(self.lbl_2)
        self.layout.addWidget(self.te_edit)
        self.layout.addLayout(self.middle_layout)
        self.middle_layout.addWidget(self.btn_clear)
        self.middle_layout.addWidget(self.btn_start)
        self.layout.addWidget(self.result)

    def setup_connections(self):
        self.le.returnPressed.connect(self.verifier)
        self.btn_start.clicked.connect(self.start)
        self.btn_clear.clicked.connect(self.clear)

    def verifier(self):
        # on contraint l'utilisateur a entrer une cle valide
        while True:
            clef = self.le.text()
            if bibliotheque.verifier(clef) or not clef:
                self.le.setText("")
                QMessageBox.warning(self, "Erreur", "Cle invalide")
                return False
            return True
            break

    def start(self):
        try:
            text = self.te_edit.toPlainText()
            clef = self.le.text()
            if self.verifier():
                self.resultat = bibliotheque.decrypter_message(text, clef)
                self.result.setHtml(self.resultat)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f" erreur lors du decryptage: {e}")

    def clear(self):
        self.le.clear()
        self.te_edit.clear()
        self.result.clear()


class ChildWindow2(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setMinimumSize(400, 400)
        self.setStyleSheet("font-size: 18px")
        self.dictionnaire = DictionnaireFrancais('mots_francais.txt')
        self.en_cours = False

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layout()
        self.add_widget_to_layout()
        self.setup_connections()

    def create_widgets(self):
        self.te_edit = QTextEdit()
        self.btn_1 = QPushButton("LAUNCH")
        self.btn_1.setStyleSheet("background-color: green; margin: 50px")
        self.te_edit2 = QTextEdit()
        self.btn_2 = QPushButton("STOP")
        self.btn_2.setStyleSheet("background-color: red; margin: 30px;")
        self.btn_3 = QPushButton("CONTINUE")
        self.btn_3.setStyleSheet("background-color: grey; margin: 30px;")

    def create_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.h_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()

    def modify_widgets(self):
        self.te_edit.setPlaceholderText("Entrer le message a dechiffre  ici : !!! minimum 11 caracteres")
        self.te_edit2.setReadOnly(True)
    def add_widget_to_layout(self):
        self.main_layout.addWidget(self.te_edit)
        self.main_layout.addLayout(self.h_layout)
        self.main_layout.addWidget(self.btn_1)
        self.main_layout.addWidget(self.te_edit2)
        self.main_layout.addLayout(self.h2_layout)
        self.h2_layout.addWidget(self.btn_2)
        self.h2_layout.addWidget(self.btn_3)

    def setup_connections(self):
        self.btn_1.clicked.connect(self.action_launch)
        self.btn_2.clicked.connect(self.action_stop)
        self.btn_3.clicked.connect(self.action_continue)
    def action_launch(self):
        message = self.te_edit.toPlainText()
        if message:
            try:
                self.en_cours = True
                self.force_s_cle(message)
                QMessageBox.information(self, "Succès", "Processus lancé avec succès")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
            finally:
                self.en_cours = False  # S'assurer que l'indicateur est réinitialisé

        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez entrer un message.")

    def verification(self, matrice):
        if not matrice or len(matrice) == 0:
            return None  # Matrice vide ou invalide

        nb_lignes = len(matrice)
        nb_colonnes = len(matrice[0]) if nb_lignes > 0 else 0

        # Verification si la matrice est rectangulaire et suffisamment grande
        if nb_colonnes == 0 or any(len(ligne) != nb_colonnes for ligne in matrice):
            return None  # Matrice non rectangulaire
        if nb_colonnes * nb_lignes < 9:
            return None  # Matrice trop petite

        mots = []
        index = 0
        for i in range(2, 11):  # On itere de 2 a 10 car on souhaite creer 9 mots
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
            index = 0  # On remet index a 0 pour le mot suivant
            # verifion si les premiers mots forme a partir de la matrice appartiennent a notre dictionnaire
        for t_mots in mots:
            if self.dictionnaire.est_mot_francais(t_mots):
                return True  # on repere un mot francais dans les premieres phrases
        return False  # aucun mot repere

    def action_stop(self):
        self.en_cours = False
        QMessageBox.information(self, "Stop", "Le processus a été arrêté")

    def action_continue(self):
        if not self.en_cours:
            message = self.te_edit.toPlainText()
            if message:
                self.en_cours = True
                self.force_s_cle(message)
            else:
                QMessageBox.warning(self, "Avertissement", "Veuillez entrer un message.")

    def check(self, toto, tt):
        return tt in toto

    def creer_ensemble(self, n):
        lig = math.factorial(n)
        ensmble = []
        i = 0
        while i < lig:
            tt = random.sample(range(n), n)
            if not self.check(ensmble, tt):
                ensmble.append(tt)
                i += 1
            else:
                continue
        return ensmble

    def force_s_cle(self, texte):
        stream = Stream_To_Textedit(self.te_edit2)
        for n in range(3, 11):
            if not self.en_cours:
                break
            trouve = False
            ENS = self.creer_ensemble(n)
            for element in ENS:
                if not self.en_cours:
                    break
                if (len(texte) / n == 0):
                    ligne = int(len(texte) / n + 1)
                    reste = 0
                else:
                    reste = len(texte) % n
                    ligne = int(math.floor(len(texte) / n) + 1)
                proba = bibliotheque.decrypt_LVLUP(texte, element, ligne, n, reste)
                if self.verification(proba):
                    tot = []
                    stream.write("Cette combinaison de mots peut être probable\n")
                    for i in range(ligne):
                        for j in range(n):
                            if proba[i][j] is not None:
                                tot.append(proba[i][j])
                    tt = ''.join(tot)
                    stream.write(f"{tt}\n")
                    stream.write(f"La clef utilisée est : {element}\n")

                    tt, ok = QInputDialog.getInt(self, "Continuer ?",
                                                 "Appuyez sur 1 pour continuer ou 2 pour arrêter :", 1, 1, 2, 1)
                    if ok and tt == 2:
                        stream.write("Félicitations, vous avez arrêté la boucle de test\n")
                        trouve = True
                        break
                    elif not ok:  # L'utilisateur a annulé la boîte de dialogue
                        stream.write("Boucle de test interrompue.\n")
                        trouve = True
                        break
                    else:
                        stream.write("Continuons la boucle de test\n")

                elif not self.verification(proba):
                    continue
                else:
                    stream.write("Message trop court. Le programme ne saurait le traiter\n")
                    break
            if trouve:
                break



class ChildWindow(QWidget):

    def __init__(self, text):
        super().__init__()
        self.setup_ui()
        self.setStyleSheet("font-size: 18px;")
        self.te_edit.setPlaceholderText(text)

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widget_to_layout()
        self.setup_connections()

    def create_widgets(self):
        self.lbl_1 = QLabel(" Entrer la cle :")
        self.lbl_2 = QLabel(" Enter le message: ")
        self.le = QLineEdit()
        self.te_edit = QTextEdit()
        self.result = QTextBrowser()
        self.btn_start = QPushButton(" Start")
        self.btn_start.setStyleSheet("background-color: green; margin: 30px")
        self.btn_clear = QPushButton(" Clear")
        self.btn_clear.setStyleSheet("background-color: darkgrey; margin: 30px")

    def create_layouts(self):
        self.layout = QVBoxLayout(self)
        self.middle_layout = QHBoxLayout()

    def modify_widgets(self):
        self.le.setPlaceholderText("Entre la cle")
        self.result.setHtml(" Le resultat s'affiche ici")

    def add_widget_to_layout(self):
        self.layout.addWidget(self.lbl_1)
        self.layout.addWidget(self.le)
        self.layout.addWidget(self.lbl_2)
        self.layout.addWidget(self.te_edit)
        self.layout.addLayout(self.middle_layout)
        self.middle_layout.addWidget(self.btn_clear)
        self.middle_layout.addWidget(self.btn_start)
        self.layout.addWidget(self.result)

    def setup_connections(self):
        self.le.returnPressed.connect(self.verifier)
        self.btn_start.clicked.connect(self.start)
        self.btn_clear.clicked.connect(self.clear)

    def verifier(self):
        # on contraint l'utilisateur a entrer une cle valide
        while True:
            clef = self.le.text()
            if bibliotheque.verifier(clef) or not clef:
                self.le.setText("")
                QMessageBox.warning(self, "Erreur", "Cle invalide")
                return False
            return True
            break

    def start(self):
        try:

            text = self.te_edit.toPlainText()
            clef = self.le.text()
            if self.verifier():
                self.resultat = bibliotheque.crypter_message(text, clef)
                self.result.setHtml(str(self.resultat))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f" erreur lors du cryptage: {e}")

    def clear(self):
        self.le.clear()
        self.te_edit.clear()
        self.result.clear()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cryptage par Transposition")
        self.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)
        self.setMinimumSize(400, 400)
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layout()
        self.add_widget_to_layout()
        self.setup_connections()

    def create_widgets(self):
        self.label = QLabel(""" BIENVENUE DANS NOTRE APPLICATION DE CRYPTAGE
                                    PAR TRANSPOSITION """)
        self.btn1 = QPushButton("CRYPTER")
        self.btn1.setStyleSheet("""
            background-color: green; margin: 10px;
        """)
        self.btn2 = QPushButton("DECRYPTER")
        self.btn2.setStyleSheet("background-color: green; margin: 10px;")
        self.btn3 = QPushButton("CRYPTANALYSE")
        self.btn3.setStyleSheet("background-color: green; margin: 10px;")

    def create_layout(self):
        self.main_layout = QVBoxLayout(self)

    def add_widget_to_layout(self):
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn1)
        self.main_layout.addWidget(self.btn2)
        self.main_layout.addWidget(self.btn3)

    def setup_connections(self):
        self.btn1.clicked.connect(self.open_win1)
        self.btn2.clicked.connect(self.open_win2)
        self.btn3.clicked.connect(self.open_win3)

    def open_win1(self):
        if self.btn1.text() == "CRYPTER":
            self.child_window = ChildWindow("Entrer le message a coder")
        else:
            self.child_window = ChildWindow("Entrer le message a decoder")
        self.child_window.setMinimumSize(400, 400)
        self.child_window.show()

    def open_win3(self):
        self.win = ChildWindow2()
        self.win.show()

    def open_win2(self):
        self.win2 = ChildWindow1("Entrer le message a decoder")
        self.win2.show()


class DictionnaireFrancais:
    def __init__(self, fichier):
        self.mots = set()
        self.charger_dictionnaire(fichier)

    def charger_dictionnaire(self, fichier):  # lis un fichier et ajoute chaques mots a l'ensemble
        with open(fichier, 'r', encoding='utf-8') as f:
            for ligne in f:
                self.mots.add(ligne.strip().lower())

    def est_mot_francais(self, mot):  # verifie si un mot est dans l'ensemble
        return mot.lower() in self.mots


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
