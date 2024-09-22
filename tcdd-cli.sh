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
    echo "	Disclaimer: This is not an official software and has no affiliation with the State Railways Of The Republic of Turkiye."
    echo "	Bilgilendirme: Türkiye Cumhuriyeti Devlet Demiryolları ile herhangi bir ilişkisi yoktur."
    echo ""
    echo "	Interrupt to exit (CTRL+C)"
    echo ""
}

# Function to prompt for parameters
prompt_parameters() {
    # Prompt for departure date
    read -p "Enter departure date and time (ex. 2024-09-23T00:00:00): " gidisTarih

    # Fetch station list and allow user to select stations
    echo "Fetching station list from TCDD API..."
    python3 train.py "$gidisTarih"
}

main() {
    print_logo
    prompt_parameters
}

main
