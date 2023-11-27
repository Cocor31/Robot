from .models import Phrase
from .config import DB
from sqlalchemy import select


class Phrase_Ctrl():
    def __init__(self) :
        db = DB()
        self.session = db.session

    def add(self, demande, reponse):
        # Check if reponse already exist
        phrase = self.get_one(demande)
        if phrase != None:
            print("Error Adding. This demande already exists !")
            return
        # Adding
        phrase = Phrase(
            demande = demande,
            reponse = reponse
        )
        self.session.add(phrase)
        self.session.commit()

    def get_all (self):
        statement = select(Phrase)
        result = self.session.scalars(statement)
        return result
    
    def get_one(self, demande):
        result = self.session.query(Phrase).filter_by(demande=demande).first()
        return result
    
    def patch(self, demande, reponse):
        # Check if demande exist
        check = self.get_one(demande)
        if check == None:
            print("Error Patching. This demande does not exists !")
            return
        # Patching
        phrase = self.session.query(Phrase).filter_by(demande=demande).first()
        phrase.reponse = reponse
        self.session.commit()

    def delete(self, demande):
        # Check if demande exist
        check = self.get_one(demande)
        if check == None:
            print("Error Deleting. This demande does not exists !")
            return
        # Deletion
        phrase = self.session.query(Phrase).filter_by(demande=demande).first()
        self.session.delete(phrase)
        self.session.commit()


#####################################################################################
#           MAIN
##################################################################################### 

if __name__ == "__main__":
    pass
    # myPhrase = Phrase_Ctrl()
    # myPhrase.add("Saluto", "Salut mon humain!")
    # myPhrase.get_all()
    # myPhrase.patch("Saluto", "Salut l'asticot")
    # myPhrase.get_all()
    # myPhrase.delete('Saluto')
    # myPhrase.get_all()
    # myPhrase.delete('Saluto')

   