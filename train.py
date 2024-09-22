import argparse
import requests
from datetime import datetime

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
    choice = int(input(f"{prompt} (Enter number): ")) - 1
    return stations[choice]
    
def parse_args():
    parser = argparse.ArgumentParser(description="An application to query TCDD API")
    parser.add_argument("gidisTarih", help="Departure date and time in format 'YYYY-MM-DDTHH:MM:SS'")
    return parser.parse_args()

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
    
    # Make API request with selected stations
    response = client.fetch_trips(
        departure["istasyonAdi"],
        arrival["istasyonAdi"],
        departure["istasyonId"],
        arrival["istasyonId"],
        args.gidisTarih
    )

    if response.status_code == 200:
        data = response.json()
        trip_list = data.get("seferSorgulamaSonucList")
        if trip_list is not None:
            for trip in trip_list:
                departure_date = trip.get("binisTarih")
                vagon_tipleri = trip.get("vagonTipleriBosYerUcret", [])
                for vagon in vagon_tipleri:
                    kalan_sayi = vagon.get("kalanSayi")
                    print(f"Binis Tarih: {departure_date}, Kalan Sayi: {kalan_sayi}")
        else:
            print("No seferSorgulamaSonucList found in the response.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
