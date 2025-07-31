import requests
import folium

# API settings
API_URL = "https://reading-opendata.r2p.com/api/v1/vehicle-positions" #Retrieves exact location of all buses in active service
API_TOKEN = "" #Generate an api key in the home page and paste it inbetween the quotation marks

# Fetch live vehicle data
response = requests.get(API_URL, params={"api_token": API_TOKEN})
data = response.json()

# Create folium map
m = folium.Map(location=[51.456, -0.969], zoom_start=13)

# Add RBUS route 17 buses as custom purple markers
for bus in data:
    if bus.get("operator") == "RBUS" and bus.get("service") == "17": 
        lat = float(bus["latitude"])
        lon = float(bus["longitude"])
        label = f'Bus {bus["vehicle"]} (Route 17)\nSeen: {bus.get("observed")}'
        
        # Custom purple icon using FontAwesome bus icon
        folium.Marker(
            location=[lat, lon],
            popup=label,
            icon=folium.Icon(color="darkpurple", icon="bus", prefix="fa")  # Built-in purple
        ).add_to(m)

# Save initial map to HTML
html_path = "live_route_17_map.html"
m.save(html_path)

# Inject auto-refresh tag and override icon color to custom purple (#371d78)
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Inject meta-refresh in <head>
html = html.replace(
    "<head>",
    '<head>\n<meta http-equiv="refresh" content="30">\n'
)

# Inject custom CSS for purple marker color
custom_css = """
<style>
    .leaflet-marker-icon {
        filter: hue-rotate(250deg) saturate(200%);
    }
</style>
</head>
"""
html = html.replace("</head>", custom_css)

# Write updated HTML
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Auto-refreshing map saved as: {html_path}")
