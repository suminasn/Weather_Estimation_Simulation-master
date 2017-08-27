Read this Document carefully before executing the program.
*************************************************
This Project simulates weather environment for a game that is coded to take place on earth. So the locations on earth only are considered for simulation of the climatic conditions.
*************************************************
Methodology
The environment is summarized by the training samples with the attributes of position, time and weather conditions. A classification model is built for weather conditions and three regression models for weather sensors measurements (Temperature/Pressure/Humidity) (training_locations.txt).
These models are used to predict the environment for the testing samples (testing_locations.txt).
*************************************************
Requirements:
1.	This application requires Python 2.7 and following python packages.
-	pandas (to load and save the data )
-	sklearn ( for machine learning model creation like linear regression model, and Random Forest Model)
-	forcastio ( to download training weather data from forcast.io and google api )
2.	Internet connection to download data
 *************************************************
Way of Execution:
1.	Run the file data_collect.py in command prompt as:
	python data_collect.py
	This creates a training data file called training_weather_data.csv in the folder /data by getting the names of those locations present in the file training_locations.txt which is present in the data folder. (If you want to collect the data of more regions, provide the names of the places along with the country names in the training_locations.txt file, save it and run the script again).
2.	Save the regions in the file testing_locations.txt in the folder /data, of which you want to simulate the climatic conditions.
3.	Run the file environment_weather_simulation.py in command prompt as:
	python environment_weather_simulation.py
	This will produce an output file called generated_weather_data.csv in the folder /data for the locations given in the file testing_locations.txt.
	This is the climatic conditions that is required to simulate the game environment.
