from pprint import pprint
from random import randint
from time import sleep
import os
from typing_extensions import Self

ENERGIE_REPRODUCTION_POISSON = 2
ENERGIE_REPRODUCTION_REQUIN = 5
ENERGIE_REQUIN_MAX = 4

class Monde:
    def __init__(self,largeur,hauteur):
        self.largeur=largeur
        self.hauteur=hauteur
        self.carte=[[None for _ in range(largeur)] for _ in range(hauteur)]
    
    def afficher_monde(self):
        for ligne in self.carte:
            for case in ligne:
                if case is None:
                    print("-",end=" ")
                elif isinstance(case,Requin):
                    print("R",end=" ")
                elif isinstance(case,Thon):
                    print("T",end=" ")
            print("\n")    
    def peupler(self, nb_poisson, nb_requin):
        thonx = randint(0,self.largeur-1)
        thony = randint(0,self.hauteur-1)
        requinx = randint(0,self.largeur-1)
        requiny = randint(0,self.hauteur-1)

        for _ in range(nb_poisson):
            while self.carte[thony][thonx] is not None:
                thonx = randint(0,self.largeur-1)
                thony = randint(0,self.hauteur-1)
            self.carte[thony][thonx] = Thon(thonx,thony)
        
        for _ in range(nb_requin):   
            while self.carte[requiny][requinx] is not None:
                    requinx = randint(0,self.largeur-1)
                    requiny = randint(0,self.hauteur-1)
            self.carte[requiny][requinx] = Requin(requinx,requiny)
    
def tour_du_monde(self):
        for ligne in self.grille:
            for elt in ligne:
                if elt is not None:
                    elt.jouer_tour(self)
"""
    def jouer_un_tour(self):
        for ligne in self.carte:
            for case in ligne:
                if isinstance(case,Thon):
                    case.vivre_une_journee(self)
                elif isinstance(case,Requin):
                    case.vivre_une_journee(self)
"""

class Thon:
    compteur = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.compteur_reproduction = 0
        Thon.compteur=+1
       
    
    def deplacement_possible(self,monde):
        list_deplacement_possible=[]
        if monde.carte[self.y][(self.x +1 )% monde.largeur] is None:
            list_deplacement_possible.append((((self.x +1 )% monde.largeur),self.y,))
        if monde.carte[self.y][(self.x -1 )% monde.largeur] is None:
            list_deplacement_possible.append((((self.x -1 )% monde.largeur),self.y,))
        if monde.carte[(self.y+1)% monde.hauteur][self.x] is None:
            list_deplacement_possible.append((self.x,(self.y+1)% monde.hauteur))
        if monde.carte[(self.y-1)% monde.hauteur][self.x] is None:
            list_deplacement_possible.append((self.x,(self.y-1)% monde.hauteur))
        return list_deplacement_possible
    
    def se_deplacer(self,monde):
        
        list_deplacement_possible = Thon.deplacement_possible(self,monde)
        if len(list_deplacement_possible)>0:
            x_avant_deplacement=self.x
            y_avant_deplacement=self.y
            deplacer=list_deplacement_possible[randint(len(list_deplacement_possible)-1)]
            self.x,self.y=deplacer
            monde.carte[deplacer[1]]

    def __del__(self):
        Thon.compteur-= 1 
    
    def se_reproduire(self,monde,x_avant_deplacement,y_avant_deplacement):
        monde.carte[y_avant_deplacement][x_avant_deplacement]=Thon(x_avant_deplacement,y_avant_deplacement)
    
    def jouer_un_tours(self,monde):
        x_avant_deplacemen,y_avant_deplacement = self.x,self.y
        if len(self.deplacement_possible(monde))>0:
            self.se_deplacer(monde)
            if self.compteur_reproduction>= ENERGIE_REPRODUCTION_POISSON:
                self.se_reproduire(monde)
                self.compteur_reproduction=0
        else:
            self.compteur_reproduction+=1





class Requin():
    compteur = 0

    def __init__(self, x, y):
        self.energie = ENERGIE_REQUIN_MAX
        self.x = x
        self.y = y
        self.energie_repro = 0
       
        
    
    def deplacement_possible(self,monde):
        list_deplacement_possible=[]
        if monde.carte[self.y][(self.x +1 )% monde.largeur] is None:
            list_deplacement_possible.append((self.y,((self.x +1 )% monde.largeur)))
        if monde.carte[self.y][(self.x -1 )% monde.largeur] is None:
            list_deplacement_possible.append((self.y,((self.x -1 )% monde.largeur)))
        if monde.carte[(self.y+1)% monde.hauteur][self.x] is None:
            list_deplacement_possible.append(((self.y+1)% monde.hauteur , self.x))
        if monde.carte[(self.y-1)% monde.hauteur][self.x] is None:
            list_deplacement_possible.append(((self.y-1)% monde.hauteur , self.x))
        return list_deplacement_possible
    
    def se_deplacer(self,monde):
        
        list_deplacement_possible = Thon.deplacement_possible(self,monde)
        if len(list_deplacement_possible)>0:
            x_avant_deplacement=self.x
            y_avant_deplacement=self.y
            deplacer=list_deplacement_possible[randint(len(list_deplacement_possible)-1)]
            self.x,self.y=deplacer

    def proies_adjacentes(self,monde):
        cases_proie = []
        if type(monde.grille[(self.y - 1)% monde.hauteur][self.x]) is Thon:
            
            cases_proie.append((self.x, (self.y - 1) % monde.hauteur))
        if type(monde.grille[(self.y + 1)% monde.hauteur][self.x]) is Thon:
            
            cases_proie.append((self.x, (self.y + 1) % monde.hauteur))
        if type(monde.grille[self.y][(self.x+1)% monde.largeur]) is Thon:
            
            cases_proie.append(((self.y),(self.x+1)% monde.largeur)) is Thon
        if type(monde.grille[self.y][(self.x-1)% monde.largeur]) is Thon:
            
            cases_proie.append(((self.x-1)% monde.largeur),(self.y)) is Thon
        return cases_proie

    def se_reproduire(self, monde, x_preced, y_preced):
        monde.carte[x_preced][y_preced] = Requin(x_preced, y_preced)

    
    def manger(self, monde):
        coups_possibles = Requin.proies_adjacentes(self, monde)
        if len(coups_possibles) > 0:
            x_precedent = self.x
            y_precedent = self.y
            coup_a_jouer = coups_possibles[randint(0, len(coups_possibles)-1)]
            self.x, self.y = coup_a_jouer
            monde.carte[self.y][self.x] = self
            monde.carte[x_precedent][y_precedent] = None
            self.energie = ENERGIE_REQUIN_MAX

    def jouer_tour(self, monde):
        x_preced, y_preced = self.x, self.y
        if self.energie == 0:
            monde.grille[self.x][self.x] = None
        elif len(self.proies_adjacentes(monde)) > 0:
            self.manger(monde)
        elif len(self.obtenir_cases_adjacente_libre(monde)) > 0:
            self.se_deplacer(monde)
        
        if self.compteur_reproduction >= ENERGIE_REPRODUCTION_REQUIN:
            self.se_reproduire(monde, x_preced, y_preced)
            self.compteur_reproduction = 0
        self.energie -= 1
        self.compteur_reproduction += 1

monde = Monde(6, 6)
monde.peupler(10, 5)
max_poisson = 0
max_requin = 0
Monde.afficher_monde(monde)
""""
while Thon.compteur != 0 and Requin.compteur != 0:
    if Thon.compteur > max_poisson:
        max_poisson = Thon.compteur
    if Requin.compteur > max_requin:
        max_requin = Requin.compteur
"""
Monde.tour_du_monde(monde)

Monde.afficher_monde(monde)

print("Nb Requins : " + str(Requin.compteur), end=" ")
print("Nb Poisson : " + str(Thon.compteur))