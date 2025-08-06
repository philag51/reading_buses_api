import requests as rq
import xml.etree.ElementTree as ET
from datetime import datetime

# Replace with your actual API key and 12 digit stop code (Paste them between the quote marks)
api_token = ""
stop_code = ""

# Build URL with API token and bus stop code
url = f"https://reading-opendata.r2p.com/api/v1/siri-sm?api_token={api_token}&location={stop_code}"

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

    print(f'Departures from {stop_name}:\n')

    # Loop over the first 10 bus entries
    for visit in visits[:10]:
        journey = visit.find('siri:MonitoredVehicleJourney', ns)

        line_ref = journey.find('siri:LineRef', ns)
        destination = journey.find('siri:DestinationName', ns)
        monitored_call = journey.find('siri:MonitoredCall', ns)
        aimed_departure = monitored_call.find('siri:AimedDepartureTime', ns) if monitored_call is not None else None

        # Parse and format time
        if aimed_departure is not None:
            aimed_time = datetime.fromisoformat(aimed_departure.text)
            time_str = aimed_time.strftime('%H:%M')  # HH:MM format
        else:
            time_str = "Unknown"

        print(f"Route {line_ref.text if line_ref is not None else '?'}: to {destination.text if destination is not None else '?'}, Expected at: {time_str}")

else:
    print("Failed to fetch data. Status code:", response.status_code)
