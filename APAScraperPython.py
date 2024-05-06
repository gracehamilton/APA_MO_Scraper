import petpy
import airflow
def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
def join_columns(df):
    cols = {}
    for c in df.columns[1:]:
        cols[c] = c[:-2]
    return df.rename(columns = cols)
class dogData():
    def __init__(self, override = False): #override to autopopulate at-risk list
        self.data = join_columns(self.getData()).groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1)).set_index("organization_animal_id")
        self.override = override
        self.data.to_csv("dogData.csv")
    def getData(self):
        pf = petpy.Petfinder('y1ojzoyO7TvfNHyXfWDZAX9rL1GUIrgbGOnqPvtzAs3FoC0S0O', 'rjK77I88buUdQmqhZ4tcc1HMOevOKgP7NdNM49Hf')
        oldest_dogs_df = pf.animals(animal_type = 'dog', status = 'adoptable', organization_id = 'MO228', return_df = True, results_per_page = 50, pages = 2, sort = '-recent')
        newest_dogs_df = pf.animals(animal_type = 'dog', status = 'adoptable', organization_id = 'MO228', return_df = True, results_per_page = 50, pages = 2, sort = 'recent')
        apamo = oldest_dogs_df.merge(newest_dogs_df, how = 'outer', on = 'id') #second half not saving
        return apamo
    def capacity(self):
        volume = len(self.data)
        if volume < 200 and self.override != True:
            print("APA Missouri has %s dogs, according to Petfinder" %volume)
        else:
            print("Capacity exceeded, see current atRisk.csv for info")
            self.overflow().to_csv("atRisk.csv")
    def overflow(self):
        picks = self.data.query('(age == "Adult" or age == "Senior") and (size == "Large" or size == "Medium")')[['url', 'gender', 'name', 'description', 'breeds.primary', 'breeds.secondary', 'breeds.mixed', 'breeds.unknown', 'primary_photo_cropped.small']]
        return picks
def main():
    test = dogData(override=True)
    test.capacity()
main()