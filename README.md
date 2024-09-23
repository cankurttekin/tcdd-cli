# tcdd-cli
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
<br>
This tool helps you to find an empty seat in Turkish Railways by making requests to TCDD API. 

<img src="/demo.png" alt="img" align="center" width=90%>

## Features
Let's you choose date, stations and goes to loop to fetch empty seats and notify when seats > 0.
It uses ASCII BEL to notify when seats available so if you disabled terminal bell sound and want to get audio feedback you may need to enable it.

## Usage
```
# Clone repository to any directory
git clone https://github.com/cankurttekin/tcdd-cli.git

# Go to tcdd-cli directory
cd tcdd-cli/

# Grant execute permission
chmod +x tcdd-cli.sh

# Run
./tcdd-cli.sh
```

# TO DO
- ~~Implement station and id lookup.~~
- ~~Run it in the background and get notified when there's an empty seat available for desired destination and time.~~
- Make it prettier. ~~> kinda??~~
- Telegram bot
