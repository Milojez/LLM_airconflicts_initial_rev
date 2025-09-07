#This script serves for sending a prompt through API and saving the responses
import json
import os
import LLM_airconflicts_initial_rev.prompt_generator as prompt_generator
from LLM_airconflicts_initial_rev.prompt_generator import prompt_fun_dict
from LLM_airconflicts_initial_rev.LLM_model_config import MODEL_CONFIGS

# ----------------PICK THE MODEL, FOLDER AND VARIABLES--------------------------------
# Setting the folder with files

# in_folder = "./Milo_code_minisky/json_files"
in_folder = "./LLM_airconflicts_initial_rev/aircraft_info_conf_2ac/detecting_conflict" #specify folder where all json files on conflicting aircraft are

out_folder = "./LLM_airconflicts_initial_rev/LLM_responses" #specify where the folder with LLM subfolders are located for saving all data.

#Setting the model
# available model : Deepseek, Llama_70b, CHAT_GPT_4o, Gemini_2_5, Sonnet_3_7, CHAT_GPT_o3_mini
MODEL = "Gemini_2_5"

# Setting variables
temperature = 0 #temperature for LLM model for inference
gen_main_prompt = "Head_exp_free_choice" # Set the function generating prompt / difficulty level regarding the case being considered for inference, "Head_exp", "Head_exp_json"
gen_json = "Head_exp_json_free_choice" # Set the function generating json prompt

#---------------------------------------- STEP 1: LOADING THE LLM MODEL AND PROMPT FUNCTION-------------------------------------------------
LLM_model_dict = MODEL_CONFIGS[MODEL]
model = LLM_model_dict["model"]
api_key = LLM_model_dict["api_key"]
provider = LLM_model_dict["provider"]
if provider == 0:
    client = LLM_model_dict["client"](api_key) # Calls the lambda to initialize the client
else:
    client = LLM_model_dict["client"](api_key, provider)

# takes the relevant prompt function based on difficulty
gen_prompt_function = prompt_fun_dict.get(gen_main_prompt)
gen_prompt_json_function = prompt_fun_dict.get(gen_json)
#---------------------------------------- STEP 2: LOADING THE FILE FROM THE PICKED FOLDER (loop) -------------------------------------------------

# Loop through every file in the folder 
for DATA_FILE in os.listdir(in_folder):
    if DATA_FILE.endswith(".json"):  # Process only JSON files
        print(f"Processing file: {DATA_FILE}")

    # Load aircraft data from JSON
    with open(f"{in_folder}/{DATA_FILE}", "r") as file:
        aircraft_data = json.load(file)

    # Load aircraft CONFLICT data from JSON
    new_DATA_FILE_name = DATA_FILE.rstrip(".json")
    CONFLICT_DATA_FILE = DATA_FILE.replace(".json", "_con.json")
    with open(f"./LLM_airconflicts_initial_rev/confl_info_ac/detecting_conflict{CONFLICT_DATA_FILE}", "r") as file:
        conflict_data = json.load(file)

    #----------------------STEP 3: GENERATING THE MAIN PROMPT-------------------
    reasoning_prompt = gen_prompt_function(aircraft_data, conflict_data)

    #-----------------STEP 4: LLM RESPONSE--------------------
    if MODEL == "Sonnet_3_7" : #Anthropic has a different was of calling functions
        reasoning_response = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": reasoning_prompt}],
            max_tokens = 5000,
            # tools=[],  # This explicitly sets the list of tools to use. Setting it to an empty list still may trigger LLM to believe it could use tools
            temperature = temperature
        )
        reasoning_text = reasoning_response.content[0].text.strip()

        for part in reasoning_response.content:
            if part.type == "tool_use":
                print("Tool calls were present:") #Checking if tool calls are present

    else: #This is rest of models
        reasoning_response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": reasoning_prompt}],
            # tools=[],  # This explicitly sets the list of tools to use. Setting it to an empty list still may trigger LLM to believe it could use tools
            temperature = temperature,
        )
        reasoning_text = reasoning_response.choices[0].message.content.strip()

        if reasoning_response.choices[0].message.tool_calls: #Checking if tool calls are present
            print("Tool calls were present:")
            print(reasoning_response.choices[0].message.tool_calls)

    #-------------------------------- STEP 5: SAVING REASONING FILE-----------------------------
    # Save reasoning separately
    os.makedirs(f"{out_folder}/{MODEL}", exist_ok=True)
    # Save reasoning separately with UTF-8 encoding
    with open(f"{out_folder}/{MODEL}/{new_DATA_FILE_name}_{MODEL}_reasoning.txt", "w", encoding="utf-8") as f:
        f.write(reasoning_text)



    # ------------------- STEP 6: GENERATE PROMPT FOR JSON GENERATION -------------------
    json_prompt = gen_prompt_json_function(reasoning_text, aircraft_data, conflict_data)

    # ------------- STEP 7: LLM RESPONSE AS A JSON------------------------- 
    if MODEL == "Sonnet_3_7" : #Anthropic has a different was of calling functions
        json_response = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": json_prompt}],
            max_tokens = 1600,
            tools=[],  # This explicitly sets the list of tools to use. Setting it to an empty list still may trigger LLM to believe it could use tools
            temperature = temperature
        )
        # Extract response text
        json_text = json_response.content[0].text.strip()

    else: #This is rest of models
        json_response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": json_prompt}],
            # tools=[],  # This explicitly sets the list of tools to use. Setting it to an empty list still may trigger LLM to believe it could use tools
            temperature = temperature
        )

        # Extract response text
        json_text = json_response.choices[0].message.content.strip()

    # Remove markdown formatting if present
    if json_text.startswith("```json"):
        json_text = json_text[7:]  # Remove ```json
    if json_text.endswith("```"):
        json_text = json_text[:-3]  # Remove closing ```

    # print(json_text)

    # -------------------STEP 8: SAVE JSON -------------------

    try:
        response_json = json.loads(json_text)  # Attempt to parse JSON

        os.makedirs(f"{out_folder}/{MODEL}/json", exist_ok=True)
        with open(f"{out_folder}/{MODEL}/json/{new_DATA_FILE_name}_{MODEL}_reasoning.json", "w", encoding="utf-8") as f:
            json.dump(response_json, f, indent=4, ensure_ascii=False)

        print("\n--- JSON Saved ---\n")

    except json.JSONDecodeError:
        print("Error: JSON output invalid. Saving raw output.")
        with open(f"{out_folder}/{new_DATA_FILE_name}_{MODEL}_raw_output.json", "w", encoding="utf-8") as f:
            f.write(json_text)

        print("Raw output saved")
