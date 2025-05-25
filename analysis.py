from AzureConnection import AzureGetAllWithStatus
from pandas import DataFrame

retired = AzureGetAllWithStatus("Retired")
active = AzureGetAllWithStatus("Active")

