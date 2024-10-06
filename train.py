import argparse
import requests
from datetime import datetime
import time
import os
import random
import sys

class TCDDAPIClient:
    def __init__(self):
        self.api_url = "https://api-yebsp.tcddtasimacilik.gov.tr"
        self.trips_endpoint = self.api_url + "/sefer/seferSorgula"
        self.stations_endpoint = self.api_url + "/istasyon/istasyonYukle"
        self.headers = {
            "Authorization": "Basic ZGl0cmF2b3llYnNwOmRpdHJhMzQhdm8u",
            "Content-Type": "application/json",
            "Host": "api-yebsp.tcddtasimacilik.gov.tr"
        }
        self.cookie = {
            "JSESSIONID": "576DCF37FCB434F6B044713AC044E28A"
        }
        
    def format_date(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").strftime("%b %d, %Y %I:%M:%S %p")
        
    def fetch_stations(self):
        body = {
            "kanalKodu":"3",
            "dil":1,
            "tarih":"Nov 10, 2011 12:00:00 AM",
            "satisSorgu":True
        }
        response = requests.post(self.stations_endpoint, headers=self.headers, json=body, cookies=self.cookie)
        if response.status_code == 200:
            return response.json().get("istasyonBilgileriList", [])
        else:
            print(f"Failed to fetch stations: {response.status_code}")
            return []

    def fetch_trips(self, departure_station, arrival_station, departure_station_id, arrival_station_id, date):
        formatted_date = self.format_date(date)
        body = {
            "kanalKodu": 3,
            "dil": 0,
            "seferSorgulamaKriterWSDVO": {
                "satisKanali": 3,
                "binisIstasyonu": departure_station,
                "binisIstasyonu_isHaritaGosterimi": False,
                "inisIstasyonu": arrival_station,
                "inisIstasyonu_isHaritaGosterimi": False,
                "seyahatTuru": 1,
                "gidisTarih": formatted_date,
                "bolgeselGelsin": False,
                "islemTipi": 0,
                "yolcuSayisi": 1,
                "aktarmalarGelsin": True,
                "binisIstasyonId": departure_station_id,
                "inisIstasyonId": arrival_station_id
            }
        }
        response = requests.post(self.trips_endpoint, headers=self.headers, json=body, cookies=self.cookie)
        return response

def display_stations(stations):
    for i, station in enumerate(stations, 1):
        #print(f"{i}. {station['istasyonAdi']}, {station['stationViewName']}")
        print(f"{i}. {station['stationViewName']}")

def select_station(stations, prompt):
    display_stations(stations)
    choice = int(input(f"\n{prompt} (Enter number): \n» ")) - 1
    return stations[choice]
    
def parse_args():
    parser = argparse.ArgumentParser(description="An application to query TCDD API")
    parser.add_argument("departure_date_input", help="Departure date and time in format 'YYYY-MM-DDTHH:MM:SS'")
    return parser.parse_args()

def notify_user(departure_date, arrival_date, economy_seat_count, economy_price, disabled_seat_count, business_seat_count, business_price):
    # Using Terminal ASCII BEL
    #print("\a")  # beep
    for _ in range(2):
        print("\a", flush=True)
        sys.stdout.flush()  # Force the output to be sent to the terminal
        for _ in range(1000000): pass  # Dummy loop for a minimal delay to play multiple beeps
    print("\033[1m\033[31m »»» Seats available for: \033[0m")
    print(f"{departure_date} ———→ {arrival_date}: "
                                + f"\n\tEconomy: {economy_seat_count} [TRY {economy_price}]" 
                                + f"\n\tDisabled: {disabled_seat_count} "
                                + f"\n\tBusiness: {business_seat_count} [TRY {business_price}]")
    #print("»»»»»»»» Seats available!")
    
def prompt_seat_type():
    print("Which seat type would you like to track?")
    print("1. Economy")
    print("2. Business")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        return "Economy"
    elif choice == "2":
        return "Business"
    else:
        print("Invalid choice. Defaulting to Economy.")
        return "Economy"
    
def main():
    args = parse_args()
    client = TCDDAPIClient()
    
    # Fetch stations and let the user choose
    stations = client.fetch_stations()
    if not stations:
        print("No stations found.")
        return
        
    print("\nSelect departure station:")
    departure = select_station(stations, "Departure station")
    print("\nSelect arrival station:")
    arrival = select_station(stations, "Arrival station")
    
    seat_type = prompt_seat_type()  # Prompt user to select seat type
    
    # Continuous loop to keep checking for available seats
    print(chr(27) + "[2J")
    #os.system('cls||clear')
    print(f"\nSearching for: {seat_type} seats from {departure["istasyonAdi"]} to {arrival["istasyonAdi"]} at {args.departure_date_input[0:10]}\n\n\n")
    while True:
        response = client.fetch_trips(
            departure["istasyonAdi"],
            arrival["istasyonAdi"],
            departure["istasyonId"],
            arrival["istasyonId"],
            args.departure_date_input
        )

        if response.status_code == 200:
            data = response.json()
            trip_list = data.get("seferSorgulamaSonucList")
            if trip_list is not None:
                for trip in trip_list:
                    #available_empty_seats = 0
                    # REFACTOR THESE LINES LATER : CODE REPEAT
                    departure_date = trip.get("binisTarih")
                    departure_date = datetime.strptime(departure_date, "%b %d, %Y %I:%M:%S %p") # Parse the string into a datetime object
                    departure_date = departure_date.strftime("%b %d, %H:%M") # remove year and format to 24 hour
                    
                    arrival_date = trip.get("inisTarih")
                    arrival_date = datetime.strptime(arrival_date, "%b %d, %Y %I:%M:%S %p") # Parse the string into a datetime object
                    arrival_date = arrival_date.strftime("%H:%M") # remove year and format to 24 hour
                    
                    economy_seat_count = 0
                    disabled_seat_count = 0
                    business_seat_count = 0
                    economy_price = 0
                    business_price = 0
                    vagon_tipleri = trip.get("vagonTipleriBosYerUcret")
                    for vagon in vagon_tipleri:
                        # Check if it's an economy wagon 2+2 Pulman (Ekonomi) or 17002
                        if ("Ekonomi" in vagon.get("vagonTip")) or (vagon.get("vagonTipId") == 17002):
                            disabled_seat_count += vagon.get("kalanEngelliKoltukSayisi")
                            economy_seat_count += vagon.get("kalanSayi") - disabled_seat_count
                            economy_price = int(vagon.get("standartBiletFiyati"))
                        # Check if business
                        elif ("Business" in vagon.get("vagonTip")) or (vagon.get("vagonTipId") == 17001):
                            business_seat_count += vagon.get("kalanSayi")
                            business_price = int(vagon.get("standartBiletFiyati"))
                    
                    # Notify user if there are available seats based on user-selected seat type
                    if economy_seat_count > 0 and seat_type == "Economy":
                        notify_user(departure_date, arrival_date, economy_seat_count, economy_price, disabled_seat_count, business_seat_count, business_price)
                    elif business_seat_count > 0 and seat_type == "Business":
                        notify_user(departure_date, arrival_date, economy_seat_count, economy_price, disabled_seat_count, business_seat_count, business_price)
                    
            else:
                print("No trip found.")
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Response: {response.text}")

        # Sleep for random seconds before making the next request
        sleep_time = random.randint(4, 42)
        
        # ANSI
        bg_color = "\033[42m"  # Black background
        fg_color = "\033[37m"  # White text
        message = f"### Waiting {sleep_time} seconds before next request"
        formatted_message = f"{bg_color}{fg_color}{message:}\033[0m"
        sys.stdout.write(f"\r{formatted_message.replace(str(sleep_time), str(sleep_time))}")
        sys.stdout.flush()
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
