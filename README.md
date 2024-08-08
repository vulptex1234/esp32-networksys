Create passwords.py in each folder
# Integrated Folder
Import this folder to your esp32

## boot.py
This file consists with these componensts below:
- Network configulation
- Establish connection
- Flag 
- main

### Network configlation
import passwords from your passwords.py. Define your SSID_NAME_*

### Establish connection
Establish connection with your SSID_NAME_* by executing connect_*_wifi().

connect_*_wifi() calls wifiscan() searchs nearby Wi-Fi signals.

flag() decides whather activate 'cm_main.py' or 'ch_main.py'

## calc.py
This file normalizes 2 parameter values(battery, number of connectabele nodes) and calculate euclidian distance.

### normalize()
Normalize battery and number of connectable nodes.

Reading battery and number of connectable nodes from 'node_data.csv', normalize these 2 parameters.
Then, write the normalized data to 'normalized_node_data.csv'

### extract_from_csv()
extract_from_csv() extracts 2 values from 'normalized_node_data.csv' and call sim_score().

### sim_score()
sim_score() calculates euclidian distance using given 2 arguments from extract_from_csv().