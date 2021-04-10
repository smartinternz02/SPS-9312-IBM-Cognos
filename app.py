from flask import Flask, request,render_template
import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "46n7O4bckzN54VwL9Uj1dNkWjEUpdFK-a6SUj4uU1l2i"
token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    date = request.form["date"]
    opens = request.form["opens"]
    high = request.form["high"]
    low = request.form["low"]
    close = request.form["close"]
   
    adjclose= request.form["adjclose"]
   
    
    


    t = [[int(date),int(opens),int(high),int(low),int(close),float(adjclose)]]
    print(t)
    payload_scoring = {"input_data": [ {"field": [["date","opens","high","low","close","adjclose"]],
                   "values": t}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/66517877-e84a-42cf-9872-f71773d310f2/predictions?version=2021-04-08', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    #output = "Negative Diabetes"
        
    
    return render_template('index.html', prediction_text= pred)


if __name__ == "__main__":
    app.run(debug=True,port=8000)
