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
        if '?' in demande or '!' in demande:
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
  
    def saluer(self):
        print("Bonjour")


#####################################################################################
#           MAIN
##################################################################################### 

if __name__ == "__main__":
    myIdiot = Robot()
   