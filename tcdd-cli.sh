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
    echo "BU YAZILIMIN TÜRKİYE CUMHURİYETİ DEVLET DEMİRYOLLARI İLE HERHANGİ BİR İLİŞKİSİ YOKTUR."
    echo ""
    echo "Turkish Train API CLI Tool"
    echo "THIS IS NOT AN OFFICIAL SOFTWARE AND HAS NO AFFILIATION WITH THE STATE RAILWAYS OF THE REPUBLIC OF TURKIYE."
    echo ""
}

# Function to prompt for parameters
prompt_parameters() {
    # Prompt for departure date
    read -p "Enter departure date and time (YYYY-MM-DDTHH:MM:SS) / Kalkış tarihini ve saati girin (YYYY-AA-GGTSsaat:dk:sn): " gidisTarih

    # Run Python script to fetch station list and allow user to select stations
    echo "Fetching station list from TCDD API..."
    python3 train.py "$gidisTarih"
}

main() {
    print_logo
    prompt_parameters
}

main
