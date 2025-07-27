
🌦️ Weather Dashboard - Modern Desktop Weather Application
A beautiful, feature-rich weather desktop application built with Python and Flet framework. Get real-time weather data, 5-day forecasts, and manage your favorite cities with a modern, intuitive interface.
Show Image
✨ Features

🌡️ Real-time Weather Data - Current temperature, humidity, wind speed, pressure
📅 5-Day Forecast - Extended weather predictions with detailed information
⭐ Favorite Cities - Save and quickly access your preferred locations
🌅 Sunrise/Sunset Times - Daily sun schedule information
🎨 Modern UI - Clean, responsive design with weather icons
🌙 Weather Icons - Visual representation of weather conditions
💾 Data Persistence - Your favorite cities are saved locally
🔄 Auto-refresh - Real-time weather updates
📱 Cross-platform - Works on Windows, macOS, and Linux

🚀 Quick Start
Prerequisites

Python 3.7 or higher
Internet connection for weather data
OpenWeatherMap API key (free)

Installation

Clone the repository
bashgit clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard

Install dependencies
bashpip install -r requirements.txt

Get your API key

Visit OpenWeatherMap
Sign up for a free account
Generate your API key


Configure API key

Open weather_app.py
Replace YOUR_API_KEY_HERE with your actual API key:

pythonself.api_key = "your_actual_api_key_here"

Run the application
bashpython weather_app.py


📱 Usage
Searching for Weather

Enter a city name in the search field
Click "Search Weather" or press Enter
View current weather and 5-day forecast

Managing Favorites

Click the ❤️ icon next to any city name to add it to favorites
Click favorite cities in the sidebar to quickly load their weather
Use the 🗑️ icon to remove cities from favorites

Understanding Weather Data

Current Temperature - Real-time temperature and "feels like"
Weather Conditions - Visual icons and descriptions
Wind Speed - Current wind speed in m/s
Humidity - Current humidity percentage
Pressure - Atmospheric pressure in hPa
Sunrise/Sunset - Daily sun schedule

🛠️ Technical Details
Built With

Python - Core programming language
Flet - Modern UI framework (Flutter for Python)
OpenWeatherMap API - Weather data provider
Requests - HTTP library for API calls
