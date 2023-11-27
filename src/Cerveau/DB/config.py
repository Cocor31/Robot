
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from .models import Base, Phrase
from sqlalchemy.orm import Session


class DB ():

    def __init__(self) :
        load_dotenv()
        self.engine = create_engine(os.getenv('ENGINE_PATH'), echo=False)
        self.create_tables()
        self.session = Session(bind=self.engine)

    def test(self):
        with self.engine.connect() as connection:
            result = connection.execute(text('select "Hello DB"'))
            print(result.all())

    def create_tables(self):
        print("TABLES SYNCHRONIZATION >>>> ")
        Base.metadata.create_all(bind=self.engine)  # <= A commenter quand développement fini

#####################################################################################
#           MAIN
##################################################################################### 

if __name__ == "__main__":
    myDB = DB()