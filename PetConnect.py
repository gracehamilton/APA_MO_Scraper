from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

url = "https://24petconnect.com/PetHarbor/getAdoptableAnimalsByLatLon"

def getTotal():
    try: 
        request = requests.post(url, headers={'Content-type': 'application/x-www-form-urlencoded'}, data="model%5BAnimalType%5D=DOG&model%5BSearchType%5D=ADOPT&model%5BLatitude%5D=38.672294&model%5BLongitude%5D=-90.533239&model%5BMiles%5D=20&model%5BLocationChanged%5D=false&model%5BURLName%5D=&model%5BAnimalFilter%5D%5BAnimalType%5D=DOG&model%5BAnimalFilter%5D%5BSearchType%5D=ADOPT&model%5BAnimalFilter%5D%5BURLName%5D=&model%5BAnimalFilter%5D%5BShelterList%5D=('APMO1'%2C'APMO')&model%5BAnimalFilter%5D%5BBreedList%5D=&model%5BAnimalFilter%5D%5BSimilarBreeds%5D=false&model%5BAnimalFilter%5D%5BGender%5D=&model%5BAnimalFilter%5D%5BAge%5D=&model%5BAnimalFilter%5D%5BSize%5D=&model%5BAnimalFilter%5D%5BSortBy%5D=&BreedReqId=")
        soup = bs(request.content.decode('utf-8'), 'html.parser')
        return int(soup('script')[0].string.replace('\r\n', "").split("=")[-1][1:-1])
    except:
        return 0

def getDataFrame(index):
    #TODO: Add try/except statements, error logging
    request = requests.post(url, headers={'Content-type': 'application/x-www-form-urlencoded'}, data="model%5BAnimalType%5D=DOG&model%5BSearchType%5D=ADOPT&model%5BLatitude%5D=38.672294&model%5BLongitude%5D=-90.533239&model%5BMiles%5D=20&model%5BIndex%5D="+str(index)+"&model%5BLocationChanged%5D=false&model%5BURLName%5D=&model%5BAnimalFilter%5D%5BAnimalType%5D=DOG&model%5BAnimalFilter%5D%5BSearchType%5D=ADOPT&model%5BAnimalFilter%5D%5BURLName%5D=&model%5BAnimalFilter%5D%5BShelterList%5D=('APMO1'%2C'APMO')&model%5BAnimalFilter%5D%5BBreedList%5D=&model%5BAnimalFilter%5D%5BSimilarBreeds%5D=false&model%5BAnimalFilter%5D%5BGender%5D=&model%5BAnimalFilter%5D%5BAge%5D=&model%5BAnimalFilter%5D%5BSize%5D=&model%5BAnimalFilter%5D%5BSortBy%5D=&BreedReqId=")
    if request.status_code == 200:
        totalSoup = bs(request.content.decode('utf-8'), 'html.parser')
        resultGrid = totalSoup.find_all('div', attrs={"class": "gridResult", "id": re.compile("Result_A(?s:.)")})
        dogsParsed = []
        for dog in resultGrid:
            dogHTML=bs(str(dog), 'html.parser')
            attrs = dogHTML('span')
            forDF = {"shelterCode": re.findall('APMO[0-9]?',str(dog.attrs['onclick']))[0]} #onclick = "Details('shelterCode', 'animal_id')"
            for attr in attrs[:-1]:
                prop, val = re.split(" ?: ",attr.string)
                val = re.sub(" $", "", val)
                forDF[prop]=val
            forDF['Description'] = getDescription(forDF["Animal id"], forDF["shelterCode"])
            dogsParsed.append(forDF)
        dogDF = pd.DataFrame(dogsParsed)
        index += 1
        return dogDF.dropna()

def getDescription(animalID, shelterID):
    request = requests.post("https://24petconnect.com/PetHarbor/getAnimalDetails", headers={'Content-type': 'application/x-www-form-urlencoded'}, data="model%5BAnimalId%5D="+animalID+"&model%5BShelterId%5D="+shelterID)
    soup = bs(request.content.decode('utf-8'), 'html.parser')
    return soup.find_all("span", attrs={"class": "text_MoreInfo details"})[0].get_text()

#print(requests.post(apamo, headers={'Content-Type': 'application/json'}, data=body, cookies={"ARRAffinity": ARRAffinity}).content.decode('utf-8'))