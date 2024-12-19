import requests

rfid_code = "sfcgvbhnjk"  # RFID modülünden alınan kod
response = requests.post(
    "http://192.168.5.22:3000/api/open-door",
    json={"rfid_code": rfid_code}
)

print(response.json())