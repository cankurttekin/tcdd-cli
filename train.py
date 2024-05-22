import argparse
import requests
from datetime import datetime

class TCDDAPIClient:
    def __init__(self):
        self.base_url = "https://api-yebsp.tcddtasimacilik.gov.tr/sefer/seferSorgula"
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

    def make_request(self, binis_istasyonu, inis_istasyonu, binis_istasyon_id, inis_istasyon_id, gidis_tarih):
        gidis_tarih_formatted = self.format_date(gidis_tarih)
        body = {
            "kanalKodu": 3,
            "dil": 0,
            "seferSorgulamaKriterWSDVO": {
                "satisKanali": 3,
                "binisIstasyonu": binis_istasyonu,
                "binisIstasyonu_isHaritaGosterimi": False,
                "inisIstasyonu": inis_istasyonu,
                "inisIstasyonu_isHaritaGosterimi": False,
                "seyahatTuru": 1,
                "gidisTarih": gidis_tarih_formatted,
                "bolgeselGelsin": False,
                "islemTipi": 0,
                "yolcuSayisi": 1,
                "aktarmalarGelsin": True,
                "binisIstasyonId": binis_istasyon_id,
                "inisIstasyonId": inis_istasyon_id
            }
        }
        response = requests.post(self.base_url, headers=self.headers, json=body, cookies=self.cookie)
        return response

def parse_args():
    parser = argparse.ArgumentParser(description="An application to query TCDD API")
    parser.add_argument("binisIstasyonu", help="Departure station")
    parser.add_argument("inisIstasyonu", help="Arrival station")
    parser.add_argument("binisIstasyonId", type=int, help="Departure station ID")
    parser.add_argument("inisIstasyonId", type=int, help="Arrival station ID")
    parser.add_argument("gidisTarih", help="Departure date and time in format 'YYYY-MM-DDTHH:MM:SS'")
    return parser.parse_args()

def main():
    args = parse_args()
    client = TCDDAPIClient()
    response = client.make_request(args.binisIstasyonu, args.inisIstasyonu, args.binisIstasyonId, args.inisIstasyonId, args.gidisTarih)

    if response.status_code == 200:
        data = response.json()
        sefer_list = data.get("seferSorgulamaSonucList")
        if sefer_list is not None:
            for sefer in sefer_list:
                binis_tarih = sefer.get("binisTarih")
                vagon_tipleri = sefer.get("vagonTipleriBosYerUcret", [])
                for vagon in vagon_tipleri:
                    kalan_sayi = vagon.get("kalanSayi")
                    print(f"Binis Tarih: {binis_tarih}, Kalan Sayi: {kalan_sayi}")
        else:
            print("No seferSorgulamaSonucList found in the response.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
