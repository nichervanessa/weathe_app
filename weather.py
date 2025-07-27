import flet as ft
import requests
import json
import datetime
from typing import Dict, Optional

class WeatherAPI:
    def __init__(self):
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.api_key = "7f8aeed7e99abbbb6ec7b12c630cb84d"

    def get_current_weather(self, city: str) -> Optional[Dict]:
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url=url, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None

    def get_forecast(self, city: str) -> Optional[Dict]:
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url=url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Forecast API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None

class WeatherApp:
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.favorite_file = "favorite_cities.json"
        self.favorites = self.load_favorites()

    def load_favorites(self):
        try:
            with open(self.favorite_file, 'r') as f:
                return json.load(f)
        except:
            return ['Duhok', 'Erbil', 'Kirkuk', 'Mosul', 'Sulaymaniah']

    def save_favorites(self):
        try:
            with open(self.favorite_file, 'w') as f:
                json.dump(self.favorites, f)
        except Exception as e:
            print(f"Error saving favorites: {e}")

    def add_favorite(self, city: str):
        if city not in self.favorites:
            self.favorites.append(city)
            self.save_favorites()

    def remove_favorite(self, city: str):
        if city in self.favorites:
            self.favorites.remove(city)
            self.save_favorites()

def weatherapp(page: ft.Page):
    page.title = "Weather Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.window.width = 1200
    page.window.height = 700
    page.window.center()
    page.scroll = ft.ScrollMode.HIDDEN
    
    # Try to set icon, but don't fail if file doesn't exist
    try:
        page.window.icon = "weather.ico"
    except:
        pass
    
    weather_app = WeatherApp()
    
    def search_weather():
        city = city_input.value.strip()
        if not city:
            status_text.value = "Please enter a city name"
            status_text.color = ft.Colors.RED_400
            page.update()
            return
        
        status_text.value = "Loading weather data..."
        status_text.color = ft.Colors.BLUE_400
        page.update()
        
        current_weather = weather_app.weather_api.get_current_weather(city)
        if current_weather:
            current_weather_card.content = create_current_weather_display(current_weather).content
            status_text.value = f"Weather data loaded for {current_weather['name']}"
            status_text.color = ft.Colors.GREEN_600
            
            # Get forecast
            forecast_data = weather_app.weather_api.get_forecast(city=city)
            if forecast_data:
                update_forecast_display(forecast_data)
        else:
            status_text.value = f"Could not find weather data for '{city}'. Please check the city name and try again."
            status_text.color = ft.Colors.RED_400
        
        page.update()

    # UI Components
    city_input = ft.TextField(
        label="Enter city name", 
        hint_text="e.g., Erbil, Duhok, Baghdad, London", 
        expand=True, 
        on_submit=lambda e: search_weather(),
        border_radius=10
    )
    
    search_button = ft.ElevatedButton(
        "Search Weather", 
        icon=ft.Icons.SEARCH, 
        on_click=lambda e: search_weather(),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600, 
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=50
    )
    
    current_weather_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.CLOUD, size=60, color=ft.Colors.GREY_400),
                ft.Text("Enter a city name and click search to view current weather", 
                       size=16, 
                       text_align=ft.TextAlign.CENTER,
                       color=ft.Colors.GREY_600)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=30,
        bgcolor=ft.Colors.BLUE_50,
        border_radius=15,
        height=320,
        alignment=ft.alignment.center
    )
    
    forecast_container = ft.Row(
        controls=[],
        scroll=ft.ScrollMode.AUTO,
        spacing=10
    )
    
    favorites_container = ft.Column()
    status_text = ft.Text("Ready to search for weather data", color=ft.Colors.GREY_600, size=14)

    def get_weather_icon(weather_code: str) -> str:
        icon_map = {
            "01d": "☀️", "01n": "🌙",  # Clear sky
            "02d": "⛅", "02n": "⛅",  # Few clouds
            "03d": "☁️", "03n": "☁️",  # Scattered clouds
            "04d": "☁️", "04n": "☁️",  # Broken clouds
            "09d": "🌧️", "09n": "🌧️",  # Shower rain
            "10d": "🌦️", "10n": "🌧️",  # Rain
            "11d": "⛈️", "11n": "⛈️",  # Thunderstorm
            "13d": "❄️", "13n": "❄️",  # Snow
            "50d": "🌫️", "50n": "🌫️",  # Mist
        }
        return icon_map.get(weather_code, "🌤️")

    def create_current_weather_display(weather_data: Dict):
        main = weather_data['main']
        weather = weather_data['weather'][0]
        wind = weather_data.get("wind", {})

        city_name = weather_data['name']
        country = weather_data['sys']['country']
        temp = round(main['temp'])
        feels_like = round(main.get('feels_like', 0))
        humidity = main.get('humidity', 0)
        pressure = main['pressure']
        wind_speed = wind.get("speed", 0)
        description = weather["description"].title()
        icon = get_weather_icon(weather["icon"])
        
        # Convert sunrise/sunset from Unix timestamp
        sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime("%I:%M %p")
        sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset']).strftime("%I:%M %p")

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"{city_name}, {country}", size=26, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                ft.Icons.FAVORITE_BORDER, 
                                icon_color=ft.Colors.RED_400, 
                                on_click=lambda e: add_to_favorites(city_name),
                                tooltip="Add to favorites",
                                icon_size=28
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(
                        datetime.datetime.now().strftime("%A, %B %d, %Y - %I:%M %p"), 
                        size=14, 
                        color=ft.Colors.GREY_500
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(icon, size=100),
                                    ft.Text(description, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(f"{temp}°C", size=54, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                                    ft.Text(f"Feels like {feels_like}°C", size=16, color=ft.Colors.GREY_600),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.BLUE_400, size=20),
                                        ft.Text("Humidity", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(f"{humidity}%", size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5
                                ),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.AIR, color=ft.Colors.GREY_600, size=20),
                                        ft.Text("Wind", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(f"{wind_speed} m/s", size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5
                                ),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.SPEED, color=ft.Colors.ORANGE_400, size=20),
                                        ft.Text("Pressure", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(f"{pressure} hPa", size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5
                                ),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.WB_SUNNY, color=ft.Colors.YELLOW_600, size=20),
                                        ft.Text("Sunrise", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(sunrise, size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5
                                ),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.NIGHTLIGHT, color=ft.Colors.PURPLE_400, size=20),
                                        ft.Text("Sunset", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(sunset, size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5
                                ),
                                expand=True
                            ),
                        ],
                        spacing=10
                    )
                ],
                spacing=15
            ),
            padding=25,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=15,
            height=320
        )

    def create_forecast_card(forecast_item: Dict):
        dt = datetime.datetime.fromtimestamp(forecast_item['dt'])
        temp = round(forecast_item['main']['temp'])
        temp_min = round(forecast_item['main']['temp_min'])
        temp_max = round(forecast_item['main']['temp_max'])
        weather = forecast_item['weather'][0]
        icon = get_weather_icon(weather['icon'])
        description = weather['description'].title()

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(dt.strftime("%a"), size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(dt.strftime("%m/%d"), size=12, color=ft.Colors.GREY_600),
                    ft.Text(icon, size=36),
                    ft.Text(f"{temp}°C", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    ft.Text(f"{temp_min}° / {temp_max}°", size=12, color=ft.Colors.GREY_600),
                    ft.Text(description, size=10, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(2, ft.Colors.BLUE_200),
            border_radius=12,
            width=130,
            margin=ft.margin.only(right=10)
        )

    def create_favorite_card(city: str):
        def load_city_weather(e):
            city_input.value = city
            search_weather()
        
        def remove_from_favorites(e):
            weather_app.remove_favorite(city=city)
            update_favorites_display()
            # Show removal confirmation
            snackbar = ft.SnackBar(
                content=ft.Text(f"Removed {city} from favorites"),
                bgcolor=ft.Colors.ORANGE_600
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.LOCATION_CITY, color=ft.Colors.BLUE_400, size=20),
                    ft.Text(city, size=16, expand=True, weight=ft.FontWeight.W_500),
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE, 
                        icon_color=ft.Colors.RED_400, 
                        on_click=remove_from_favorites, 
                        tooltip="Remove from favorites",
                        icon_size=20
                    )
                ],
                spacing=10
            ),
            padding=12,
            bgcolor=ft.Colors.GREY_50,
            border_radius=10,
            margin=ft.margin.only(bottom=8),
            on_click=load_city_weather,
            ink=True,
            border=ft.border.all(1, ft.Colors.GREY_200)
        )

    def update_forecast_display(forecast_data: Dict):
        forecast_container.controls.clear()
        # Show next 5 days
        daily_forecasts = []
        seen_dates = set()
        
        for item in forecast_data['list']:
            dt = datetime.datetime.fromtimestamp(item["dt"])
            date_str = dt.strftime("%Y-%m-%d")

            if date_str not in seen_dates and len(daily_forecasts) < 5:
                # Prefer forecasts around noon (12:00)
                if dt.hour >= 12 or len(daily_forecasts) == 0:
                    daily_forecasts.append(item)
                    seen_dates.add(date_str)
        
        for forecast_item in daily_forecasts:
            forecast_container.controls.append(create_forecast_card(forecast_item))
        
        page.update()

    def add_to_favorites(city: str):
        if city not in weather_app.favorites:
            weather_app.add_favorite(city)
            update_favorites_display()
            snackbar = ft.SnackBar(
                content=ft.Text(f"Added {city} to favorites! ⭐"),
                bgcolor=ft.Colors.GREEN_600
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()
        else:
            snackbar = ft.SnackBar(
                content=ft.Text(f"{city} is already in your favorites"),
                bgcolor=ft.Colors.ORANGE_600
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

    def update_favorites_display():
        favorites_container.controls.clear()
        favorites_container.controls.append(
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_400, size=24),
                    ft.Text("Favorite Cities", size=20, weight=ft.FontWeight.BOLD)
                ],
                spacing=10
            )
        )
        
        if weather_app.favorites:
            for city in weather_app.favorites:
                favorites_container.controls.append(create_favorite_card(city))
        else:
            favorites_container.controls.append(
                ft.Container(
                    content=ft.Text("No favorite cities yet", size=14, color=ft.Colors.GREY_500),
                    padding=20,
                    alignment=ft.alignment.center
                )
            )
        
        page.update()

    # Main page layout
    page.add(
        ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.WB_SUNNY, color=ft.Colors.ORANGE_400, size=32),
                            ft.Text(
                                "Weather Dashboard", 
                                size=32, 
                                weight=ft.FontWeight.BOLD, 
                                color=ft.Colors.BLUE_800
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15
                    ), 
                    padding=ft.padding.only(bottom=20)
                ),
                
                # Search section
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    city_input,
                                    search_button
                                ],
                                spacing=15
                            ),
                            status_text
                        ],
                        spacing=10
                    ),
                    padding=25,
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=15,
                    margin=ft.margin.only(bottom=20),
                    border=ft.border.all(1, ft.Colors.GREY_200)
                ),
                
                # Main content area
                ft.Row(
                    controls=[
                        # Weather and forecast section
                        ft.Column(
                            controls=[
                                current_weather_card,
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_600, size=24),
                                                    ft.Text("5-Day Forecast", size=20, weight=ft.FontWeight.BOLD)
                                                ],
                                                spacing=10
                                            ),
                                            forecast_container
                                        ],
                                        spacing=15
                                    ),
                                    padding=25,
                                    bgcolor=ft.Colors.GREY_50,
                                    border_radius=15,
                                    margin=ft.margin.only(top=20),
                                    border=ft.border.all(1, ft.Colors.GREY_200)
                                )
                            ],
                            expand=3
                        ),
                        
                        # Favorites section
                        ft.Container(
                            content=favorites_container,
                            expand=1,
                            padding=25,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=15,
                            margin=ft.margin.only(left=20),
                            border=ft.border.all(1, ft.Colors.GREY_200)
                        )
                    ]
                )
            ],
            expand=True,
            spacing=0
        )
    )

    # Initialize favorites display
    update_favorites_display()
    
    # Load weather for first favorite city on startup
    if weather_app.favorites:
        city_input.value = weather_app.favorites[0]
        search_weather()

if __name__ == "__main__":
    ft.app(target=weatherapp, assets_dir="assets")