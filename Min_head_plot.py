import os
import json
from Min_head_change import *
import matplotlib.pyplot as plt
import numpy as np
# Define the directories containing the JSON files for each model
chatgpt_folder = "./LLM_airconflicts_initial_rev/LLM_responses/CHAT_GPT_4o/heading_change"
gemini_folder = "./LLM_airconflicts_initial_rev/LLM_responses/Gemini_2_5/heading_change"

# Define the folder containing the JSON files
json_aircraft_folder = "./LLM_airconflicts_initial_rev/aircraft_info_conf_2ac/heading_change"

# Initialize a dictionary to store the results in a list under the key "minimal_heading_changes"
results = {}

# Function to process files in the LOL folder
def process_lol_files(folder_path):
    for filename in os.listdir(folder_path):
        # Check if the file is a JSON file
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            # Load the aircraft data from the JSON file
            with open(file_path, "r") as file:
                aircraft_data = json.load(file)

            # Ensure there are at least two flights in the data
            if len(aircraft_data) >= 2:
                flight1 = aircraft_data[0]
                flight2 = aircraft_data[1]

                # Find the minimal heading change for the current pair of flights
                result = find_min_heading_change(flight1, flight2)

                # Extract the minimal_heading_change_degrees from the result
                minimal_heading_change_degrees = result.get("minimal_heading_change_degrees")
                Flight1_CAS = aircraft_data[0]["CAS (knots)"]

                # Store the result in the dictionary under the key "minimal change"
                results[Flight1_CAS] = {}
                results[Flight1_CAS]["Flight1_CAS"] = Flight1_CAS
                results[Flight1_CAS]["minimal change"] = minimal_heading_change_degrees
                
# Process the files in the folder
process_lol_files(json_aircraft_folder)

# #ADDING chnages in headign from LLMs
def LLM_heading_change(folder_path, name):
    for filename in os.listdir(folder_path):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)

                # Load the aircraft data from the JSON file
                with open(file_path, "r") as file:
                    LLM_json_data = json.load(file)
                results[LLM_json_data["conflicting_pairs"][0]["FLIGHT_1_CAS"]][name] = LLM_json_data["conflicting_pairs"][0]["heading_change"]

#Adding LLM headings
# Define the directories containing the JSON files for each model
# gemini_folder = "./Milo_code_minisky/LLM_responses/Head_exp/Head_exp_sp/Gemini_2_5/json"
# chatgpt_folder = "./Milo_code_minisky/LLM_responses/Head_exp/Head_exp_sp/CHAT_GPT_4o/json"
gemini_folder = "-"
chatgpt_folder = ".-"

LLM_heading_change(gemini_folder, "Gemini_2_5")
LLM_heading_change(chatgpt_folder,"CHAT_GPT_4o")

# Now you can print the dictionary to see the results
# print(results)

#PLOT
# Initialize lists to store data
flight1_cas = []
minimal_change = []
gemini_2_5 = []
chat_gpt_4o = []

# Extract the data from the dictionary
for cas, values in results.items():
    print(values)
    flight1_cas.append(values['Flight1_CAS'])
    minimal_change.append(values['minimal change'] if values['minimal change'] is not None else np.nan)  # Handle None
    gemini_2_5.append(values["Gemini_2_5"])
    chat_gpt_4o.append(values['CHAT_GPT_4o'])

# # Create the plot
# plt.figure(figsize=(10, 6))

# # Scatter plot for each set of values (using dots)
# plt.scatter(flight1_cas, minimal_change, label='Minimal Change', marker='o')
# plt.scatter(flight1_cas, gemini_2_5, label='Gemini_2_5', marker='x')
# plt.scatter(flight1_cas, chat_gpt_4o, label='CHAT_GPT_4o', marker='s')

# # Label the axes
# plt.xlabel('Flight1 CAS Velocity (Knots)')
# plt.ylabel('Heading Change (Degrees)')

# # Title and legend
# plt.title('Heading Change vs. Flight1 CAS Velocity')
# plt.legend()

# # Show grid and plot
# plt.grid(True)
# plt.show()

# Create and save the first plot (without Gemini_2_5)
plt.figure(figsize=(10, 6))
plt.scatter(flight1_cas, minimal_change, label='Minimal Change', marker='o')
plt.scatter(flight1_cas, chat_gpt_4o, label='CHAT_GPT_4o', marker='s',color='green')

plt.xlabel('Flight1 CAS Velocity (Knots)')
plt.ylabel('Heading Change (Degrees)')
plt.title('Heading Change vs. Flight1 CAS Velocity / chat_gpt_4o')
plt.legend()
plt.grid(True)
plt.savefig('./plots/plot_chat_gpt_4o.png')  # Save the plot as a PNG file
plt.close()  # Close the figure to avoid overlap with the next plot

# Create and save the second plot (without CHAT_GPT_4o)
plt.figure(figsize=(10, 6))
plt.scatter(flight1_cas, minimal_change, label='Minimal Change', marker='o')
plt.scatter(flight1_cas, gemini_2_5, label='Gemini_2_5', marker='x')

plt.xlabel('Flight1 CAS Velocity (Knots)')
plt.ylabel('Heading Change (Degrees)')
plt.title('Heading Change vs. Flight1 CAS Velocity / gemini_2_5')
plt.legend()
plt.grid(True)
plt.savefig('./plots/plot_gemini_2_5.png')  # Save the plot as a PNG file
plt.close()  # Close the figure to avoid overlap with other plots