import os
import mysql
import mysql.connector
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

db = mysql.connector.connect(host="localhost", user="root",
                               passwd="myPASSWORD", database='traffic',
                               auth_plugin='mysql_native_password')
cur = db.cursor()
with open('/home/seetharaman/Documents/Traffic Volume Estimation/objects/model','rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict',methods=["POST","GET"])
def predict():
    input_features = [x for x in request.form.values()]
    features_values = [np.array(input_features)]
    names = [['holiday','temp','rain','snow','weather','year','month','day','hours','minutes','seconds']]
    
    holiday = str(request.form["holiday"])
    temp = float(request.form["temp"])
    rain = int(request.form["rain"])
    snow = int(request.form["snow"])
    weather = str(request.form["weather"])
    year = int(request.form["year"])
    month = int(request.form["month"])
    day = int(request.form["day"])
    hours = int(request.form["hours"])
    mins = int(request.form["minutes"])
    secs = int(request.form["seconds"])

    data = pd.DataFrame(features_values, columns = names)
    prediction = int(model.predict(data))
    estimate = prediction

    query = ("insert into traffic_info(holiday, temp, rain, snow, weather, yr, month, day, hour, mins, secs, estimate) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    vals = (holiday, temp, rain, snow, weather, year, month, day, hours, mins, secs, estimate)
    cur.execute(query, vals)
    db.commit()
    db.close()
    return render_template("demo.html",prediction_text = str(prediction))

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(port=port, debug=True,use_reloader = False)