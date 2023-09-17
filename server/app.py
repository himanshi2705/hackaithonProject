from flask import Flask, request, jsonify
import sys
import pickle
import json
import numpy as np
from flask_cors import CORS
__model = None
__cropnames= None
__data_columns =None

#loading the pickle file of the model 

def load_saved_artifacts():
    print("loading saved artifacts...start")
    
    #loading the crop names from column file
    global __data_columns 
    global __cropnames#cropnames is global so that it can be used outside 

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __cropnames = __data_columns[5:]  # first 4 columns are parameters hence ignore them
    print(__cropnames)
    
    #making __model global so that it can be used outside the function
    global __model
    if __model is None:
        with open('./artifacts/MoistPredModel2.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")


#function to predict the moisture of the soil using the values 

def getMoisture(cropname, timeinMin, tempreture, air_hum, pressure, windSpeed):
    try:
        loc_index = __data_columns.index(cropname.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = timeinMin
    x[1] = tempreture
    x[2] = air_hum
    x[3] = pressure
    x[4] = windSpeed
    if loc_index >= 0:
        x[loc_index] = 1
        
    # print(x)

    return __model.predict([x])[0]


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "hi"

#this is for the normal request 
@app.route('/predict_soil_moisture', methods=['GET', 'POST'])
def predict_soil_moisture():
    timeinMin= int(request.form['timeinMin'])
    tempreture= (request.form['tempreture'])
    air_hum= (request.form['air_hum'])
    pressure= (request.form['pressure'])
    windSpeed=(request.form['windSpeed'])
    x=getMoisture('maize',timeinMin, tempreture, air_hum, pressure, windSpeed)
    print(x)
    # print(timeinMin)
    # print(tempreture)
    # print(air_hum)
    # print(pressure)
    # print(windSpeed)
    response = jsonify({
        'estimated_moisture': float(x)
    })


    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

#API FOR PREDICT MOISTURE USING POST METHOD 
#access request form data and typecast into the data type which model can understand
#call the model and return response in the json format 
@app.route('/predictmoisture', methods=['POST'])
def predictmoisture():
    crop= str(request.form['cropname'])
    time= int(request.form['time'])
    tempreture= float(request.form['tempreture'])
    airmoisture= float(request.form['airmoisture'])
    pressure= float(request.form['pressure'])
    wind= float(request.form['wind'])
    resTemp = getMoisture(crop, time, tempreture, airmoisture, pressure, wind)
   


    response = jsonify({
        "estimated_moisture":  float(resTemp)
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response




if __name__ == "__main__":
    print("Starting Python Flask Server Soil Moisture Prediction...")
    load_saved_artifacts()
    print(getMoisture('maize', 192, 26, 50, 101, 2.17))
    
    app.run()