from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import datetime

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
            imageURL = "https://24petconnect.com" + dogHTML('img')[0]['src']
            attrs = dogHTML('span')
            forDF = {"shelterCode": re.findall('APMO[0-9]?',str(dog.attrs['onclick']))[0]} #onclick = "Details('shelterCode', 'animal_id')"
            forDF['imglink'] = imageURL
            for attr in attrs[:-1]:
                prop, val = re.split(" ?: ",attr.string)
                val = re.sub(" $", "", val)
                prop = re.sub(" ", "_", prop)
                if prop == "Brought_to_the_shelter":
                    val = datetime.date.fromisoformat(val.replace(".", "-"))
                elif prop == "Age":
                    years = 0 if len(re.findall(r'[0-9]+ year[s]?', val)) == 0 else int(re.findall(r'[0-9]+',re.findall(r'[0-9]+ year[s]?', val)[0])[0])
                    months = 0 if len(re.findall(r'[0-9]+ month[s]?', val)) == 0 else int(re.findall(r'[0-9]+',re.findall(r'[0-9]+ month[s]?', val)[0])[0])
                    weeks = 0 if len(re.findall(r'[0-9]+ week[s]?', val)) == 0 else int(re.findall(r'[0-9]+',re.findall(r'[0-9]+ week[s]?', val)[0])[0])
                    forDF['Age_in_months'] = int(years*12 + months + int(weeks/4))
                forDF[prop]=val
            #forDF['Description'], weight = getDescriptionandWeight(forDF["Animal_id"], forDF["shelterCode"])
            #forDF['Weight'] = 0.0 if len(weight) == 0 else float(re.search(r'[0-9]*\.[0-9]*', weight[0]).group(0))
            dogsParsed.append(forDF)
        dogDF = pd.DataFrame(dogsParsed)
        index += 1
        return dogDF.dropna()

def getDescriptionandWeight(APALink):
    request = requests.get(APALink)
    soup = bs(request.content.decode('utf-8'), 'html.parser')
    info = soup.find_all("div", attrs={"class": "apa-side-group-item"})
    print(info)
    #weight = re.findall(r"Weight: [0-9]*?\.?[0-9]+? lbs", info)
    #return (soup.find_all("span", attrs={"class": "text_MoreInfo details"})[0].get_text(), weight)

#TODO: create separate method for data cleaning?
#getDescriptionandWeight("https://apamo.org/adopt/adoptable-pets/?petID=A279214")