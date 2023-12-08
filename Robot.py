#!./env/bin/python
from src.Cerveau.Cerveau import Cerveau
from src.MissMeteo import MissMeteo
import os
from dotenv import load_dotenv

class Robot:

    cerveau = Cerveau()
    meteo = MissMeteo()
    phrase =""
    mot_sortie= None
    
    def __init__(self) :
        self.load_params()
        self.saluer()
        self.ecoute()

    def load_params(self):
        load_dotenv()
        self.mot_sortie = os.getenv('MOT_DE_SORTIE')

    def ecoute(self) :
        while self.phrase.upper() != self.mot_sortie:
            self.phrase = input()
            self.checkPhrase(self.phrase)
            
    def checkPhrase(self, demande):
        if 'oublie la phrase' in demande.lower():
            self.oublier(demande) 
        elif 'remplace la phrase' in demande.lower():
            self.replacer(demande) 
        elif 'affiche tes connaissances' in demande.lower() :
            self.affiche_connaissances()
        elif '?' in demande or '!' in demande:
            if self.meteo.is_meteo_request(demande):
                print(self.meteo.dis_moi(demande))
                return
            reponse = self.cerveau.cherche(demande)
            if  reponse != None:
                print(reponse)
            else:
                self.apprendre(demande)

    def apprendre(self, demande):
        print("Je ne sais pas quoi répondre")
        reponse_phrase = input()
        if ":"in reponse_phrase:
            reponse = reponse_phrase.split(":")[-1].strip()
            self.cerveau.enregistre(demande, reponse)
            print("Merci pour l'information")
  
    def saluer(self):
        print("Bonjour")

    def affiche_connaissances(self):
        phrases = self.cerveau.phrase.get_all()
        for phrase in phrases:
            print(phrase)

    def oublier(self, demande):
        if ":"in demande:
            demande_to_delete = demande.split(":")[-1].strip()
            self.cerveau.oubli(demande_to_delete)
            print("D'accord, j'ai oublié '{0}' !".format(demande_to_delete))
        else:
            print("Tu ne m'as pas précisé quoi oublier avec les ':'")

    def replacer(self, demande):
        if ":"in demande:
            demande_to_replace = demande.split(":")[-1].strip()
            reponse_to_replace = self.cerveau.cherche(demande_to_replace)
            if reponse_to_replace != None:
                print("Que dois-je répondre maintenant ?")
                reponse_phrase = input()
                if ":"in reponse_phrase:
                    reponse_phrase = reponse_phrase.split(":")[-1].strip()
                self.cerveau.remplace(demande_to_replace, reponse_phrase)
                print("D'accord, j'ai remplaçé la réponse à la demande '{0}' par '{1}' !".format(demande_to_replace, reponse_phrase))
            else: 
                print("Je ne connais pas la demande '{0}'".format(demande_to_replace))
        else:
            print("Tu ne m'as pas précisé la demande  à remplacer avec les ':'")





#####################################################################################
#           MAIN
##################################################################################### 

if __name__ == "__main__":
    myIdiot = Robot()
   