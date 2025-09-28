from PetConnect import getDataFrame, getTotal
import math
import pandas as pd
from datetime import datetime as dt
#from SQLAlchemyConnect import SQLLoad
from AzureConnection import AzureLoad
import sys

if __name__=="__main__":
    link = lambda r: "https://apamo.org/adopt/adoptable-pets/?petID="+r
    total = getTotal()
    today = dt.now().strftime(r'%Y%m%d_%H%M')
    reloads = math.ceil(total/30)
    totaldf = pd.DataFrame(columns= ["imglink", "Animal_id", "Name", "Gender", "Breed", "Animal_type", "Age", "Brought_to_the_shelter", "Located_at", "Distance", "shelterCode"])
    for i in range(reloads):
        totaldf = pd.concat([totaldf, getDataFrame(i * 30)], ignore_index=True)
    totaldf.drop("Animal_type", axis=1,inplace=True)
    totaldf.drop("shelterCode", axis=1, inplace=True)
    totaldf.insert(2, "APALink", totaldf["Animal_id"].apply(link))
    totaldf.insert(len(totaldf.columns)-1, "Last_Modified_Date_Time", [dt.now()]*total)
    #totaldf.to_csv("output/dogData_%s.csv" %today, index=False, sep=";")
    #SQLLoad(totaldf)
    AzureLoad(totaldf)