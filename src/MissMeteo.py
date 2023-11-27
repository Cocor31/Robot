#!./env/bin/python
from meteofrance_api import MeteoFranceClient
import datetime
import time
import requests
import pandas as pd
import re



class MissMeteo():
    def __init__(self):
        self.use_public_ip=True
        self.default_city = "Paris"
        self.default_language = "fr"
        self.split_reg ="-|'|\?| "
        self.api = MeteoFranceClient()

    def is_meteo_request(self, phrase):
        """
        Fonction to be used ouside of this module to detect if the weather is requested
        """
        question_found = False
        verbes = ["faire", "fait", "fera", "avoir", "aura"]
        mots =["beau", "soleil", "temps", "temperature", "temperatures", "pluie", "nuages", "froid", "chaud"]
        verbes_pluie = ["pleut", "pleuve", "pleuvra"]

        mot_found= list(set(mots).intersection(re.split(self.split_reg, phrase.lower())))
        verbe_found= list(set(verbes).intersection(re.split(self.split_reg, phrase.lower())))
        verbe_pluie_found= list(set(verbes_pluie).intersection(re.split(self.split_reg, phrase.lower())))

        if "?" in phrase:
            question_found = True
        
        if question_found:
            if (len (mot_found) > 0 and len (verbe_found) > 0) or len(verbe_pluie_found) > 0:
                return True
        
        return False

    def dis_moi(self, question):
        # Déduction ville et forcast day de la question
        ville = ville_demandee(question)
        forcast = self.moment_demande(question)

        # Recherche données météo
        ville_trouvee, meteo, err_txt =self.cherche(ville=ville, forcast=forcast)

        # Interprétation données météo
        if not err_txt:
            txt = interprete_meteo(forcast=forcast, ville=ville_trouvee , meteo=meteo)
        else:
            txt = err_txt

        return txt

    def cherche(self, ville=None, forcast=None):
        """
        forcast should be None for actual Weather or Integer as day offset. 0 for forcast of the actual day
        """
        err_txt = None
        ville_trouvee = None
        meteo = None

        if ville == None or ville == "":
            ville = self.get_user_city()

        # Define place
        try:
            list_places = self.api.search_places(ville)
            first_place = list_places[0]
            ville_trouvee = first_place.name
        except IndexError:
            err_txt = "Je ne trouve pas la ville de {0} ! N'y a t-il pas une erreur dans le nom ?".format(ville)
        
        # Request meteo data
        try:
            meteo = self.request(forcast=forcast, place=first_place)
        except:
            err_txt = "Je n'arrive pas à contacter Évelyne Dhéliat, pourrais-tu me redemmander plus tard ?".format(ville)

        return ville_trouvee, meteo, err_txt
    
    def request(self, forcast, place):
        if forcast != None:
            # Prevision
            response = self.api.get_forecast_for_place(place, language=self.default_language)
            return response.daily_forecast[forcast]
        else:
            # Observation en direct
            return self.api.get_observation_for_place(place, language=self.default_language)
        
    def get_user_city(self):
        if self.use_public_ip:
            # Get Public IP
            ip = requests.get('https://api.ipify.org').content.decode('utf8')

            # Get City with IP
            r = requests.get(url= 'http://ip-api.com/json/{0}'.format(ip) )
            query = r.json()
            return query['city']
        else:
            return self.default_city

    def moment_demande(self, phrase):
        """
        Return 'forcast' found in 'phrase'.
        forcast returned could be None for Now, 0 for Today, 1 for Tomorrow, ect..
        """
        forcast=None

        if " fait " in phrase.lower():
            forcast=None

        if ' aujourd' in phrase.lower():
            forcast = 0
        elif " après-demain " in phrase.lower() or " après demain " in phrase.lower():
            forcast = 2
        elif " demain " in phrase.lower():
            forcast = 1
        else :
            jours = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]
            jour= list(set(jours).intersection(re.split(self.split_reg, phrase.lower())))

            if len(jour) >0:
                index_jour_meteo = int(index_jour(jours, jour[0]))
                index_jour_aujourdhui= int(StrDateDelta(nb_day_delta = 0, format_date= "%w"))
                if index_jour_meteo <= index_jour_aujourdhui:
                    forcast = index_jour_meteo - index_jour_aujourdhui + 7
                else:
                    forcast = index_jour_meteo - index_jour_aujourdhui
        return forcast

#####################################################################################
#           FUNCTIONS
##################################################################################### 
def ville_demandee(phrase):
    ville = None
    if "à " in phrase.lower():
        ville = phrase.split("à")[-1].replace("?","").strip().split(" ")[0].strip()
    return ville

def index_jour(jours, target):
    for index, jour in enumerate(jours):
        if jour == target:
            return index
        
def interprete_meteo(forcast, ville, meteo):
    try:
        # String jour
        if forcast == None:
            str_jour = "Actuellement"
        elif forcast == 0:
            str_jour = "Aujourd'hui"
        elif forcast == 1:
            str_jour = "Demain"
        elif forcast < 7:
            jour_number = StrDateDelta(forcast, format_date='%w', sens='after')
            str_jour = jour_en_lettre(jour_number)
        else:
            str_jour= "Le {0}".format(StrDateDelta(forcast, format_date='%d/%m/%Y', sens='after'))
        
        # String temps
        if forcast != None:
            tpm_conj = 'futur'
            desc = meteo['weather12H']['desc'].lower()
        else:
            tpm_conj = 'présent'
            desc = meteo.weather_description.lower()

        if desc.startswith("peu"):
            desc = "un {0}".format(desc)

        if "averses" in desc or "eclaircies" in desc:
            str_temps =  "il y {0} des {1}".format(conjugue("avoir",tpm_conj),desc)
        elif "pluie" in desc:
            str_temps =  "il y {0} une {1}".format(conjugue("avoir",tpm_conj),desc)
        else:
            str_temps =  "le temps {0} {1}".format(conjugue("être",tpm_conj),desc)

        # String températures  
        if forcast != None:
            str_temperatures = "les températures s'étendront de {0}°C à {1}°C".format(meteo['T']['min'],
                                                                                      meteo['T']['max'])
        else:
            str_temperatures = "il fait {0}°C".format(meteo.temperature)

        # Assemblage Final
        Phrase = "{0} à {1}, {2} et {3}".format(str_jour, ville, str_temps, str_temperatures )

    except AttributeError:
        return "Je ne trouve pas d'information météo pour la ville de {0}".format(ville)
    return Phrase

def jour_en_lettre(day_number):
    jours = ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
    jour = jours[int(day_number)]
    return jour

def StrDateDelta(nb_day_delta = 1, format_date= "%Y%m%d", str_date_from = None, sens= 'before'):
    """
    argument 'sens' prend les valeurs 'before' ou 'after'
    """
    if str_date_from is None:
        # Si pas de date spécifiée, on part de la date d'aujourd'hui
        obj_date_from = datetime.datetime.today()
    else:
        obj_date_from = datetime.datetime.strptime(str_date_from, format_date)#On transforme une date string en datetime
    if sens == 'after':
        obj_date_delta = obj_date_from + datetime.timedelta(days=nb_day_delta)
    else:
        obj_date_delta = obj_date_from - datetime.timedelta(days=nb_day_delta)

    str_date_delta = obj_date_delta.strftime(format_date)

    return str_date_delta

def conjugue(verbe, tpm_conj):
    data = {'verbe': ['avoir', 'être'],
            'présent': ['a', 'est'],
            'futur':['aura', 'sera']
        } 
  
    # Create DataFrame 
    df = pd.DataFrame(data)

    # Search verbe for tpm_conj
    index_verbe = df.loc[df['verbe'] == verbe].index[0]
    verbe_conjg = df.at[index_verbe, tpm_conj]

    return verbe_conjg


#####################################################################################
#           MAIN
##################################################################################### 

if __name__ == "__main__":

    myMiss = MissMeteo()

    print(myMiss.dis_moi("Quel temps fait-il"))
    time.sleep(5)
    print(myMiss.dis_moi("Quel temps fait-il Mercredi"))
    time.sleep(5)
    print(myMiss.dis_moi("Quel temps fait-il à Bordeaux aujourd'hui"))
    time.sleep(5)
    print(myMiss.dis_moi("Fera t-il beau samedi à Paris"))
    time.sleep(5)
    print(myMiss.dis_moi("Quel temps est-t-il censé faire à Niort Jeudi"))
    time.sleep(5)
    print(myMiss.dis_moi("Est-ce qu'il fait beau"))
    time.sleep(5)
    print(myMiss.dis_moi("Est-ce qu'il fera soleil à Nancy après demain?"))