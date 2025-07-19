from AzureConnection import AzureGetAllWithStatus, AzureGetSchemas
from pandas import DataFrame
from datetime import datetime as dt
today = dt.now().strftime(r'%Y%m%d_%H%M')

retired = AzureGetAllWithStatus("Retired")
active = AzureGetAllWithStatus("Active")

retired.to_excel("output/dogData_%s_Retired.xlsx" %today, index=False)
active.to_excel("output/dogData_%s_Active.xlsx" %today, index=False)