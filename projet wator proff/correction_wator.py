from random import randint, choice
from time import sleep
import os

class Monde:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[ None for _ in range(largeur)] for _ in range(hauteur)]
    
    def afficher_monde(self):
        for ligne in self.grille:
            for case in ligne:
                if case is None:
                    print("-", end=" ")
                elif isinstance(case, Requin):
                    print("X", end=" ")
                else:
                    print("o", end=" ")
            print("\n")

    def peupler(self, nb_poisson, nb_requin):
        for _ in range(nb_poisson):
            x_aleat = randint(0, self.largeur - 1)
            y_aleat = randint(0, self.hauteur -1)
            while self.grille[y_aleat][x_aleat] is not None:
                x_aleat = randint(0, self.largeur - 1)
                y_aleat = randint(0, self.hauteur - 1)
            self.grille[y_aleat][x_aleat] = Poisson(x_aleat, y_aleat)
        for _ in range(nb_requin):
            x_aleat = randint(0, self.largeur - 1)
            y_aleat = randint(0, self.hauteur -1)
            while self.grille[y_aleat][x_aleat] is not None:
                x_aleat = randint(0, self.largeur - 1)
                y_aleat = randint(0, self.hauteur - 1)
            self.grille[y_aleat][x_aleat] = Requin(x_aleat, y_aleat)
    
    def jouer_un_tour(self):
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case, Poisson):
                    case.vivre_une_journee(self)

class Poisson:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energie_repro = 0
    
    def deplacement_possible(self, monde):
        """
        Attention /!\ Fonction qui a possiblement un bug
        """
        liste_coups_possibles = []
        if monde.grille[(self.y + 1) % monde.largeur ][self.x] is None:
            liste_coups_possibles.append(((self.y + 1) % monde.largeur, self.x))
        if monde.grille[(self.y - 1) % monde.largeur ][self.x] is None:
            liste_coups_possibles.append(((self.y - 1) % monde.largeur, self.x))
        if monde.grille[self.y][(self.x + 1) % monde.hauteur] is None:
            liste_coups_possibles.append((self.y, (self.x + 1) % monde.hauteur))
        if monde.grille[self.y][(self.x - 1) % monde.hauteur] is None:
            liste_coups_possibles.append((self.y, (self.x - 1) % monde.hauteur))
        return liste_coups_possibles
    
    def se_deplacer(self, monde):
        """
        Attention /!\ Fonction qui a possiblement un bug
        """
        x_preced = self.x
        y_preced = self.y
        coups_possibles = self.deplacement_possible(monde)
        coup_choisi = choice(coups_possibles)
        monde.grille[coup_choisi[0]][coup_choisi[1]] = self
        self.x = coup_choisi[0]
        self.y = coup_choisi[1]
        monde.grille[x_preced][y_preced] = None
        
    def vivre_une_journee(self, monde):
        x_preced = self.x
        y_preced = self.y
        deplacement_effectue = False
        self.energie_repro += 1
        if len(self.deplacement_possible(monde)) > 0:
            self.se_deplacer(monde)
            deplacement_effectue = True
        if self.energie_repro > 3 and deplacement_effectue:
            monde.grille[x_preced][y_preced] = Poisson(x_preced, y_preced)
            self.energie_repro = 0
    
class Requin(Poisson):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energie = 5
    
    def proie_adjacentes(self, monde):
        """
        Attention /!\ Fonction qui a possiblement un bug
        """
        liste_coups_possibles = []
        if type(monde.grille[(self.y + 1) % monde.largeur ][self.x]) == Poisson:
            liste_coups_possibles.append(((self.y + 1) % monde.largeur, self.x))
        if type(monde.grille[(self.y - 1) % monde.largeur ][self.x]) == Poisson:
            liste_coups_possibles.append(((self.y - 1) % monde.largeur, self.x))
        if type(monde.grille[self.y][(self.x + 1) % monde.hauteur]) == Poisson:
            liste_coups_possibles.append((self.y, (self.x + 1) % monde.hauteur))
        if type(monde.grille[self.y][(self.x - 1) % monde.hauteur]) == Poisson:
            liste_coups_possibles.append((self.y, (self.x - 1) % monde.hauteur))
        return liste_coups_possibles

    def manger(self, monde):
        """
        Attention /!\ Fonction qui a possiblement un bug
        """
        x_preced = self.x
        y_preced = self.y
        coups_possibles = self.proie_adjacentes(monde)
        coup_choisi = choice(coups_possibles)
        monde.grille[coup_choisi[0]][coup_choisi[1]] = self
        self.x = coup_choisi[0]
        self.y = coup_choisi[1]
        monde.grille[x_preced][y_preced] = None
        self.energie += 4
        if self.energie > 10:
            self.energie = 10
    
    def vivre_une_journee(self, monde):
        x_preced = self.x
        y_preced = self.y
        a_mange = False
        deplacement_effectue = False
        self.energie_repro += 1
        if self.energie == 0:
            monde.grille[self.x][self.y] = None
        elif len(self.proie_adjacentes(monde)) > 0:
            self.manger(monde)
            a_mange = True
        elif len(self.deplacement_possible(monde)) > 0:
            self.se_deplacer(monde)
            deplacement_effectue = True
        if self.energie_repro > 3 and (deplacement_effectue or a_mange):
            monde.grille[x_preced][y_preced] = Requin(x_preced, y_preced)
            self.energie_repro = 0
        self.energie -= 1

            
monde = Monde(6,6)
monde.peupler(10,4)


while True:
    monde.jouer_un_tour()
    monde.afficher_monde()
    sleep(0.2)
    os.system("clear")
  
  
def setup():
    pass

def draw():
    pass