from pandas import DataFrame
import re
from AzureConnection import getConnString, AzureGetSchemas

#lambda function for splitting mixed breeds/clearing mix data
breeds = lambda b: re.split(' and |[ ]?&[ ]?', re.sub(' ?[M|m]ix', "", b))
