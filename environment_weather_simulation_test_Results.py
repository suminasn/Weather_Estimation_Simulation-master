
'''
    The program is designed to simulate weather conditions of a game
    and analyse the test results.
    Copyright (C) <2017>  <Sumina SN>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
'''

######Headers#####

from __future__ import division

import datetime
import os
import pandas
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
import data_collect
from data_collect import download_location_info
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score,f1_score,precision_score,classification_report,confusion_matrix,recall_score

os.environ['TZ'] = 'UTC'

##################Regression Models for Temperature, Humidity and Pressure##################
############################################################################################

def get_temperature_model(df):

    temp_linr_model = linear_model.LinearRegression(fit_intercept=True, normalize=True)
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    temp_y = df[['temp']].values

    temp_linr_model.fit(input_x, temp_y)    
    return temp_linr_model

def get_humidity_model(df):

    hum_linr_model = linear_model.LinearRegression(fit_intercept=True, normalize=True)
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    hum_y = df[['hum']].values

    hum_linr_model.fit(input_x, hum_y)
    return hum_linr_model

def get_pressure_model(df):

    pres_linr_model = linear_model.LinearRegression(fit_intercept=True, normalize=True)
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    pres_y = df[['pres']].values

    pres_linr_model.fit(input_x, pres_y)
    return pres_linr_model

##################Classification Model for Climatic conditions##################
############################################################################################

def get_condition_model(df):

    cond_rf_model = RandomForestClassifier()
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    cond_y = df[['cond']].values

    cond_rf_model.fit(input_x, cond_y)

    weighted_prediction = cond_rf_model.predict(input_x)
    
    print ("Condition Model Statistics : ")
    print 'Accuracy:', accuracy_score(cond_y, weighted_prediction)
    print 'F1 score:', f1_score(cond_y, weighted_prediction,average='weighted')
    print 'Recall:', recall_score(cond_y, weighted_prediction,average='weighted')
    print 'Precision:', precision_score(cond_y, weighted_prediction,average='weighted')
    print '\n clasification report:\n', classification_report(cond_y, weighted_prediction)
    print '\n confussion matrix:\n',confusion_matrix(cond_y, weighted_prediction)
    
    return cond_rf_model

##################Main##################

def main():
    # Please specify training data file path here
    df = pandas.read_csv('data/training_weather_data.csv')

    # Generating models for weather predictions
    # using linear regression for floating point labels
    # and Random Forest model for string labels
    temp_model = get_temperature_model(df)
    pres_model = get_pressure_model(df)
    hum_model = get_humidity_model(df)
    cond_model = get_condition_model(df)


    # Generating weather data in the form of dictionary - Prediction
    if temp_model and pres_model and hum_model and cond_model:
        print ("Model generation successful")
        return 1
    else:
        print ("Model generation failed. Re run the script to regenerate the model.")
    return 0

if __name__ == '__main__':
    ret = main()
    if ret == 1:
        print ("success")
    else:
        print ("Failed")
