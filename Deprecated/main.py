import petpy
import os
import sys
print(os.curdir)
sys.path.append(os.path.relpath("config"))
from config import load_config # type: ignore
config = load_config()

def sjoin(x): return '%'.join(x[x.notnull()].astype(str))
def join_columns(df):
    cols = {}
    for c in df.columns[1:]:
        cols[c] = c[:-2]
    return df.rename(columns = cols)

class dogData():
    def __init__(self, override = False): #override to autopopulate at-risk list
        self.data = join_columns(self.getData()).groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1)).set_index("organization_animal_id")
        self.data.insert(1, "APA_url", "https://apamo.org/adopt/adoptable-pets/?petID=" + self.data.index.values[:])
        for i in range(len(self.data["description"])):
            self.data["description"][i] = self.data["description"][i].replace("&amp;#39;", "\'").replace("amp;", "").replace("&amp;amp;", "&")
        for i in range(len(self.data["name"])):
            self.data["name"][i] = self.data["name"][i].replace("&#39;", "\'")
        self.override = override
    def getData(self):
        pf = petpy.Petfinder(**config)
        oldest_dogs_df = pf.animals(animal_type = 'dog', status = 'adoptable', organization_id = 'MO228', return_df = True, results_per_page = 50, pages = 2, sort = '-recent')
        newest_dogs_df = pf.animals(animal_type = 'dog', status = 'adoptable', organization_id = 'MO228', return_df = True, results_per_page = 50, pages = 2, sort = 'recent')
        apamo = oldest_dogs_df.merge(newest_dogs_df, how = 'outer', on = 'id')
        return apamo
    def toCSV(self, columns = ['APA_url', 'gender', 'name', 'size', 'description', 'breeds.primary', 'breeds.secondary', 'breeds.mixed', 'published_at', 'status_changed_at', 'primary_photo_cropped.small']):
        self.data[columns[:]].to_csv("output/dogData.csv", header=False, sep=";")
    def capacity(self):
        volume = len(self.data)
        if volume < 200 and self.override != True:
            print("APA Missouri has %s dogs, according to Petfinder" %volume)
        else:
            print("Capacity exceeded, see current atRisk.csv for info")
            self.overflow().to_csv("output/atRisk.csv", header=False, sep=";")
    def overflow(self):
        picks = self.data.query('(age == "Adult" or age == "Senior") and (size == "Large" or size == "Medium")')[['APA_url', 'gender', 'name', 'description', 'breeds.primary', 'breeds.secondary', 'breeds.mixed', 'published_at', 'status_changed_at', 'primary_photo_cropped.small']]
        return picks
if __name__ == '__main__':
    test = dogData(override=True)
    test.capacity()