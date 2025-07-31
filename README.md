# reading_buses_api
A collection of some coding projects I did with Reading Buses open data
The API and data is free to access at the expense of £0! To access the API, create an account at https://reading-opendata.r2p.com/ 

Files:
17tracker.py:

17tracker.py is file that pinpoints all the active buses on the 17 bus route in Reading including the vehicle no. and time last seen
I'm working on adding a feature where the map automatically refreshes in real time similar to the Reading Buses app

rgbus_stops.py:

This file generates a json list of all the bus stops served by Reading Buses services as well as bus stops in the surrounding Berkshire areas 
served by other operators (Thames Valley, Thames Travel and Carousel). The key parts of the list include location_code which is a 12 digit code
unique to every bus stop. To find a specific bus stop, in the list press CTRL + F and enter the name of the bus stop you are trying to find

rgstop_predictions.py

This file shows the earliest predicted arrival time of max 10 buses from the specified bus stop in 24hr HH:MM format. 
The code outputs:
Bus route number
Destination
Predicted arrival time

In the code at the end of the url, and the 12 digit code of the specific bus stop you want to see times for which can be found in the list outputted by
the rgbus_stops.py file.
If no bus times are returned, it's for one of few reasons:

Your API Key is invalid,
You entered an invalid bus stop code,
The API is down,
There's no buses for that time (E.g some bus services do not come on Sundays, public holidays or late evenings)


