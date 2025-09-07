#This script is used for saving info on conflciting aircraft once the bluesky simulation is satrted
import requests
import json

# URL of your FastAPI server
url = "http://127.0.0.1:8000/all"  # Change if the server runs on a different host/port

# Send request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    data = response.json()  # Convert response to JSON

    # Save to a file (formatted JSON)
    output_file = "./Milo_code_minisky/json_files_aircraft/2ac/Head_exp/Head_exp_sp/Head_exp_sp30.json"
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)  # Pretty-print JSON

    print("Aircraft states Head_exp_sp30 saved to: ", output_file)
else:
    print(f"Error: {response.status_code}")

