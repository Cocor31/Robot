from .DB.controller import Phrase_Ctrl


class Cerveau:

    def __init__(self) :
        self.phrase= Phrase_Ctrl()
        
    def enregistre(self, demande, reponse):
        self.phrase.add(demande, reponse)

    def cherche(self, demande):
        phrase = self.phrase.get_one(demande)
        if phrase == None:
            return None
        return phrase.reponse
    
    def remplace(self, demande, reponse):
        self.phrase.patch(demande, reponse)
    
    def oubli(self, demande):
        self.phrase.delete(demande)


#####################################################################################
#           MAIN
##################################################################################### 

if __name__ == "__main__":
    pass

    # myCerveau = Cerveau()
    # print(myCerveau.cherche("Salut"))
    # myCerveau.enregistre("Bonjour", "Bonjour !")
    # print(myCerveau.cherche("Bonjour"))