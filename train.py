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
        print(f"{i}. {station['istasyonAdi']}, {station['stationViewName']} (ID: {station['istasyonId']})")

def select_station(stations, prompt):
    display_stations(stations)
    choice = int(input(f"\n{prompt} (Enter number): \n» ")) - 1
    return stations[choice]
    
def parse_args():
    parser = argparse.ArgumentParser(description="An application to query TCDD API")
    parser.add_argument("departure_date_input", help="Departure date and time in format 'YYYY-MM-DDTHH:MM:SS'")
    return parser.parse_args()

def notify_user():
    # Using Terminal ASCII BEL
    #print("\a")  # beep
    for _ in range(2):
        print("\a", flush=True)
        sys.stdout.flush()  # Force the output to be sent to the terminal
        for _ in range(1000000): pass  # Dummy loop for a minimal delay to play multiple beeps
    print("\033[1m\033[31m »»» Seats available: \033[0m")
    #print("»»»»»»»» Seats available!")
    
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
    
    # Continuous loop to keep checking for available seats
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
                    departure_date = trip.get("binisTarih")
                    vagon_tipleri = trip.get("vagonTipleriBosYerUcret", [])
                    for vagon in vagon_tipleri:
                        disabled_seat_count = vagon.get("kalanEngelliKoltukSayisi", 0)
                        business_seat_count = vagon.get("kalanYatakSayisi", 0)
                        empty_seat_count = vagon.get("kalanSayi", 0) - disabled_seat_count - business_seat_count

                        #kalan_sayi = vagon.get("kalanSayi")
                        if empty_seat_count > 0:
                            notify_user()
                            print(f"{departure_date} -- Seats: {empty_seat_count}, Disabled: {disabled_seat_count}, Business: {business_seat_count} ")
                            
            else:
                print("No trip found.")
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Response: {response.text}")

        # Sleep for random seconds before making the next request
        sleep_time = random.randint(8, 60)
        #print(f"\n\n═════════════════Waiting {sleep_time} seconds before next request═════════════════\n")
        
        # ANSI escape codes
        bg_color = "\033[40m"  # Black background
        fg_color = "\033[37m"  # White text
        message = f"\n### Waiting {sleep_time} seconds before next request"
        formatted_message = f"{bg_color}{fg_color}{message:}\033[0m"
        print(formatted_message + "\n")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
