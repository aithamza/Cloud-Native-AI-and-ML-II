
import json
import requests
import pandas as pd


data = pd.read_csv('sample_inference_data.csv')
data = data.drop(columns=['Timestamp', 'Location', 'Future_weather_condition'])
#data = data.drop(columns=['Future_weather_condition'])
url = 'http://bee078e8-0366-454a-8606-adc321d1be6e.eastus.azurecontainer.io/score'
headers = {'Content-Type':'application/json'}


for i in range(len(data)):
            inference_data = data.values[i].tolist()
            inference_data = json.dumps({"data": [inference_data]})
            r = requests.post(url, data=inference_data, headers=headers)
            print(str(i)+str(r.content))

