import json
from extractData import extractData

data = extractData('0D4B49BFC8AE91C961373E686DCF3405')
print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))