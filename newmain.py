from PetConnect import getDataFrame, getTotal
import math
import pandas as pd

link = lambda r: "https://apamo.org/adopt/adoptable-pets/?petID="+r
total = getTotal()
reloads = math.ceil(total/30)
totaldf = pd.DataFrame(columns= ["Animal_id", "Name", "Gender", "Breed", "Animal_type", "Age", "Brought_to_the_shelter", "Located_at", "Distance", "shelterCode", "Description", "Weight"])
#TODO: pull weight, traits from actual APA website
for i in range(reloads):
    totaldf = pd.concat([totaldf, getDataFrame(i * 30)], ignore_index=True)
totaldf.drop("Animal_type", axis=1,inplace=True)
totaldf.insert(1, "APALink", totaldf["Animal_id"].apply(link))
totaldf.to_csv("output/dogData.csv", index=False, sep=";")