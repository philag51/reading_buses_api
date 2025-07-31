import requests as rq
import xml.etree.ElementTree as ET
from datetime import datetime

# URL with XML bus data
url = "https://reading-opendata.r2p.com/api/v1/siri-sm?api_token={add api key here}&location={add 12 digit bus stop code here}" #add your API key and any 12 digit bus stop code from the list of bus stop - make sure to remove the curly brackets

# Fetch XML from the API
response = rq.get(url)

if response.status_code == 200:
    # Parse XML and define namespace
    ns = {'siri': 'http://www.siri.org.uk/siri'}
    root = ET.fromstring(response.content)

    # Find all <MonitoredStopVisit> entries
    visits = root.findall('.//siri:MonitoredStopVisit', namespaces=ns)

    # Extract stop name
    stop_monitoring_delivery = root.find('.//siri:StopMonitoringDelivery', ns)
    stop_name_elem = stop_monitoring_delivery.find('siri:MonitoringName', ns)
    stop_name = stop_name_elem.text if stop_name_elem is not None else "Unknown Stop"

    print('Departures from', stop_name)

    # Loop over the first 10 bus entries
    for visit in visits[:10]:
        journey = visit.find('siri:MonitoredVehicleJourney', ns)

        line_ref = journey.find('siri:LineRef', ns)
        destination = journey.find('siri:DestinationName', ns)
        departure_elem = journey.find('siri:OriginAimedDepartureTime', ns)

        # Extract text safely
        line_text = line_ref.text if line_ref is not None else "N/A"
        destination_text = destination.text if destination is not None else "N/A"

        # Convert departure time
        if departure_elem is not None and departure_elem.text:
            try:
                departure_time = datetime.fromisoformat(departure_elem.text)
                departure_text = departure_time.strftime("%H:%M")
            except ValueError:
                departure_text = "Invalid time"
        else:
            departure_text = "N/A"

        print(f"Route: {line_text}, Destination: {destination_text}, Departure: {departure_text}")
else:
    print("Failed to fetch bus data.")
