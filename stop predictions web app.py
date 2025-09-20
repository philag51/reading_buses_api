from flask import Flask, render_template, jsonify
import requests as rq
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

api_key = "" #Paste your API Key
stop_code = "" #Paste bus stop code

# Map route numbers to brands
route_brands = {
    "1": "Jetblack",
    "2": "Lime", "2a": "Lime",
    "3": "Leopard",
    "4": "Lion", "4a": "Lion",
    "5": "Emerald", "6": "Emerald", "6a": "Emerald",
    "9": "Buzz", "9a": "Buzz", "9b": "Buzz", "18": "Buzz",
    "10": "Ruby",
    "11": "Bronze",
    "13": "Orange", "14": "Orange",
    "15": "Sky Blue", "15a": "Sky Blue", "16": "Sky Blue",
    "17": "Purple",
    "19a": "Little Oranges", "19b": "Little Oranges", "19c": "Little Oranges",
    "20": "White Knight",
    "21": "Claret",
    "22": "Pink", "25": "Pink", "25a": "Pink",
    "23": "Berry", "24": "Berry",
    "26": "Yellow",
    "28": "Aqua", "28a": "Aqua",
    "29": "Little Berries", "29a": "Little Berries",
    "33": "Royal Blue",
    "50": "Greenwave",
    "300": "Hospital P&R",
    "500": "WT P&R",
    "600": "Mereoak P&R", "650": "Mereoak P&R",
    "701": "London Line", "702": "London Line",
    "703": "Flighhtline"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bus-data')
def get_bus_data():
    url = f"https://reading-opendata.r2p.com/api/v1/siri-sm?api_key={api_key}&location={stop_code}"
    response = rq.get(url)

    if response.status_code == 200:
        ns = {'siri': 'http://www.siri.org.uk/siri'}
        root = ET.fromstring(response.content)

        stop_monitoring_delivery = root.find('.//siri:StopMonitoringDelivery', ns)
        stop_name_elem = stop_monitoring_delivery.find('siri:MonitoringName', ns)
        stop_name = stop_name_elem.text if stop_name_elem is not None else "Unknown Stop"

        visits = root.findall('.//siri:MonitoredStopVisit', namespaces=ns)

        results = []
        for visit in visits[:10]:
            journey = visit.find('siri:MonitoredVehicleJourney', ns)

            line_ref_elem = journey.find('siri:LineRef', ns)
            destination_elem = journey.find('siri:DestinationName', ns)
            monitored_call = journey.find('siri:MonitoredCall', ns)
            aimed_departure_elem = monitored_call.find('siri:AimedDepartureTime', ns) if monitored_call is not None else None

            route_number = line_ref_elem.text.lower() if line_ref_elem is not None else "?"
            destination = destination_elem.text if destination_elem is not None else "?"
            if aimed_departure_elem is not None:
                aimed_time = datetime.fromisoformat(aimed_departure_elem.text)
                time_str = aimed_time.strftime('%H:%M')
            else:
                time_str = "Unknown"

            # Generate logo path
            brand = route_brands.get(route_number, "UnknownBrand")
            logo_path = f"/static/RB_Routes_Logos/{brand.replace(' ', '').lower()}.png"

            results.append({
                "route": route_number.upper(),  # Display route in uppercase
                "destination": destination,
                "time": time_str,
                "logo": logo_path
            })

        return jsonify({
            "stop_name": stop_name,
            "departures": results
        })

    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
