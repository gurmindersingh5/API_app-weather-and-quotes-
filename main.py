import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.config import Config
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '550')


class Home(ScreenManager):
    def get_quote(self):
        response = requests.get("https://api.kanye.rest")
        response.raise_for_status()
        data = response.json()
        quote = data["quote"]
        if len(quote) > 105:
            quote = "Quote too long to print. Try Refreshing!!!"
        self.ids.label_1.text = quote

    def get_weather(self):
        allnames = self.ids.input1.text.split(",")
        limit = 1
        key = "d333727602d91309ee5e4eb3eb49496d"
        calling_lat_lon = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={allnames[0]},{allnames[1]}&limit={limit}&appid={key}")
        calling_lat_lon.raise_for_status()
        lat_lon = calling_lat_lon.json()
        calling_weather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat_lon[0]['lat']}&lon={lat_lon[0]['lon']}&units=metric&appid={key}")
        calling_weather.raise_for_status()
        weather_data = calling_weather.json()

        self.ids.weather_label.text = f"Weather in {weather_data['name']}:\n Weather: {weather_data['weather'][0]['main']}\n Temperature: {weather_data['main']['temp']} °C\n Feels_like: {weather_data['main']['feels_like']} °C"


myurl = "http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}"

KV = Builder.load_string("""
Home:
    name: "kayne_says"
    Screen:
        BoxLayout:
            size_hint: 1,1
            orientation: 'vertical'
            background_color: "white"
            BoxLayout:
                background_color: "white"
                size_hint:1, .8
                text: "Kanye Says..."
                orientation: 'vertical'
                
                Label:
                    id: label_1
                    text_size: root.width, None
                    size: self.texture_size
                    font_size:'65'
                    padding: 90,90
                    multiline: True 
                    # halign: 'center'
                    # valign: 'top'
                    text: ""
                    canvas.before:
                        Rectangle:
                            source: 'background.png'
                            pos: self.pos
                            size: (550,900)
                        
                        
            BoxLayout:
                orientation: 'vertical'
                background_color: "white"
                size_hint: None, None
                height: "160"
                GridLayout:
                    padding : (0,0,0,0)
                    pos_hint: {"center_x": .5}
                    cols: 5
                    rows: 1
                    row_force_default: True
                    row_default_height : 150
                    Label:
                        text: ""
                        size_hint: None, None
                        size: 100, 1
                    Label:
                        text: ""
                        size_hint: None, None
                        size: 100, 1
                    Button:
                        size_hint: None, None
                        background_color: 1,1,1,0
                        size: "150", "150"
                        # pos_hint: {"center_y":.5}
                        text: "a"
                        on_release: root.get_quote()
                        Image:
                            allow_stretch:True
                            size:self.parent.size
                            source: 'kanye.png'
                            pos:self.parent.pos
                    Label:
                        text: ""
                        size_hint: None, None
                        size: 10, 1
                    Button:
                        text: "Weather page -->"
                        size_hint: None, None
                        size: 250, 60
                        pos_hint: {"center_y": .9}
                        on_release:            
                            app.root.current = "weather"
        
    Screen:
        name: "weather"
        BoxLayout:
            size_hint: 1, .7
            pos_hint: {"center_y":.6}
            Label:
                id: weather_label
                text: ""
                hint_text: "fff"
                text_size: root.width, root.height
                size: self.texture_size
                font_size:'50'
                padding: 10,10
                multiline: True 
                halign: 'center'
                valign: 'middle'
                canvas.before:
                    Color:
                        rgba: .4,.5,.9,1
                    Rectangle:
                        id: c1
                        pos: self.pos
                        size: (600,900)
        BoxLayout:
            size_hint: 1, .3
            orientation: 'vertical'
            TextInput:
                hint_text:"City,Country(Ex: Toronto,CA)"
                id: input1
                multiline: False
                size_hint: 1, None
                height: "50dp"
                pos_hint: {"center_x": .5}
            Button:
                text: "Get Weather Info"
                on_release:
                    root.get_weather()
                
    

""")


class mainapp(App):
    def build(self):
        return KV


start = mainapp()
start.run()
