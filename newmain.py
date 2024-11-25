from PetConnect import getDataFrame, getTotal
import math
import pandas as pd

link = lambda r: "https://apamo.org/adopt/adoptable-pets/?petID="+r
total = getTotal()
reloads = math.ceil(getTotal()/30) #getTotal is wrong -- pull global variable from site script
totaldf = pd.DataFrame(columns= ["Animal id", "Name", "Gender", "Breed", "Animal type", "Age", "Brought to the shelter", "Located at", "Distance", "shelterCode", "Description"])
#TODO: 
for i in range(reloads):
    totaldf = pd.concat([totaldf, getDataFrame(i * 30)], ignore_index=True)
totaldf.insert(1, "APALink", totaldf["Animal id"].apply(link))
totaldf.to_csv("output/dogData.csv", index=False, sep=";")