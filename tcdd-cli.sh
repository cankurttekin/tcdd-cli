#!/bin/bash

print_logo() {
cat << "EOF"
                                                                       
 /$$$$$$$$/$$$$$$  /$$$$$$$  /$$$$$$$         /$$$$$$  /$$      /$$$$$$
|__  $$__/$$__  $$| $$__  $$| $$__  $$       /$$__  $$| $$     |_  $$_/
   | $$ | $$  \__/| $$  \ $$| $$  \ $$      | $$  \__/| $$       | $$  
   | $$ | $$      | $$  | $$| $$  | $$      | $$      | $$       | $$  
   | $$ | $$      | $$  | $$| $$  | $$      | $$      | $$       | $$  
   | $$ | $$    $$| $$  | $$| $$  | $$      | $$    $$| $$       | $$  
   | $$ |  $$$$$$/| $$$$$$$/| $$$$$$$/      |  $$$$$$/| $$$$$$$$/$$$$$$
   |__/  \______/ |_______/ |_______/        \______/ |________/______/
                                                                       
                                                                       
                                                                                                                                                                  
EOF
    echo "Tren API Sorgu CLI Aracı"
    echo "BU YAZILIMIN TÜRKİYE CUMHURİYETİ VE TÜRKİYE CUMHURİYETİ DEVLET DEMİRYOLLARI İLE HERHANGİ BİR İLİŞKİSİ YOKTUR."
    echo ""
    echo "Turkish Train API Query CLI Tool"
    echo "THIS IS NOT AN OFFICIAL SOFTWARE AND HAS NO AFFILIATION WITH THE REPUBLIC OF TURKIYE OR THE STATE RAILWAYS OF THE REPUBLIC OF TURKIYE."
    echo ""
}

# Function to prompt for parameters
prompt_parameters() {
    read -p "Enter departure station / Kalkış istasyonunu girin: " binisIstasyonu
    read -p "Enter arrival station / Varış istasyonunu girin: " inisIstasyonu
    read -p "Enter departure station ID / Kalkış istasyonu ID girin: " binisIstasyonId
    read -p "Enter arrival station ID / Varış istasyonu ID girin: " inisIstasyonId
    read -p "Enter departure date and time (YYYY-MM-DDTHH:MM:SS) / Kalkış tarihini ve saati girin (YYYY-AA-GGTSsaat:dk:sn): " gidisTarih
}

main() {
    print_logo
    prompt_parameters

    # Make API request with provided parameters
    python3 train.py "$binisIstasyonu" "$inisIstasyonu" "$binisIstasyonId" "$inisIstasyonId" "$gidisTarih"
}

main
