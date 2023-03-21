from flask import Flask
from settings import token, tokenGiph
import requests

app = Flask(__name__)

##used to define the root URL path for the Flask application. When a user visits the root URL path,
# Flask will call the view function associated with this decorator and return its output.
@app.route('/')
def hello():
	return '<div style="text-align: center; font-size: 30px; background-color: #ADD8E6;">Hello User!<br>' \
		   'If you want to check the weather in some city all over the world,<br>' \
		   'just add to the URL /weather/city_name</div>'

#This code defines a route for the "/weather/<city>" path of the application,
# where <city> is a variable that can be any string.
# When the user visits a path of the form "/weather/<city>", the weather() function is called,
# which sends an HTTP GET request to the OpenWeatherMap API to retrieve weather data for the specified city.
# The temperature data is extracted from the response and returned to the user along with an image.
@app.route('/weather/<city>')
def weather(city):
	url = "https://api.openweathermap.org/data/2.5/weather"
	params = {'q': city, 'units': 'metric', 'appid': token}
	response = requests.get(url = url, params = params) #making an HTTP GET request to the specified URL with the specified parameters, using the requests library.

	# Get the temperature from the OpenWeatherMap API response
	temperature = response.json()['main']['temp']

	if temperature <= 0:
		search_term = 'snow man'
	elif 1 < temperature <= 20:
		search_term = 'warm cloths'
	elif 21 < temperature <= 26:
		search_term = 'beach'
	else:
		search_term = 'hell'

	# Search for a relevant GIF based on the temperature using the Giphy API
	giphy_url = "https://api.giphy.com/v1/gifs/search"
	giphy_params = {'api_key': tokenGiph, 'q': search_term, 'limit': 1}
	giphy_response = requests.get(url = giphy_url, params = giphy_params)
	giphy_data = giphy_response.json()

	# Get the URL of the first GIF in the Giphy API response
	gif_url = giphy_data['data'][0]['images']['fixed_height']['url']

	# Build the HTML string to return to the user, including the temperature and GIF
	html = '<div style="text-align: center; font-size: 30px;">Temperature in ' + city + ' is: ' + str(
		temperature) + 'C <br><br><br>'
	html += '<img src="' + gif_url + '"></div>'

	return html

if __name__ == "__main__":
	app.run()
