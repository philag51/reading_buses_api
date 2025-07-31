import requests

api_url = 'https://reading-opendata.r2p.com/api/v1/busstops?api_token=' #Paste your API key after the equals sign

response = requests.get(api_url) #Retrieves data from the API
data = response.json() #Specifies that data must be in json format

print(data) #Prints full json list
