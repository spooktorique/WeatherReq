import argparse
import random
import time
from pythonosc import udp_client
import pyowm # Python Open Weather Map
from pyowm.owm import OWM
#Update with your token key for OWM here.
owm = OWM("TOKEN HERE")
mgr = owm.weather_manager()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server IP")
    parser.add_argument("--port", type=int, default=9000, help="Send to the following port")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

    while True:
        #get weather data
	#Add the desired location Latitude and Longitude
        one_call = mgr.one_call(lat=00, lon=-1)
        temp = one_call.current.temperature('celsius').get('temp') #Ex.: 7.7
        humid = one_call.current.humidity
        general = one_call.current.status
        print(general)
        print("Temperature: ", temp, "c")
        print("Humidity: ", humid, "%")
        #Set temperature and humidity values
        isHumid = False
        isHot = False
        if humid > 91:
            isHumid = True
            print("humid")
        if temp > 10:
            isHot = True
            print("hot")

        #send data via OSC, uses in game parameters WeatherTemp and WeatherHumid.
        client.send_message("/avatar/parameters/WeatherTemp", isHot)
        client.send_message("/avatar/parameters/WeatherHumid", isHumid)
        time.sleep(300)
