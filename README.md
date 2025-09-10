# Initial Review of LLMs for Aircraft Conflicts

This repository contains scripts and data used for the **initial testing of five Large Language Models (LLMs)** in the context of aircraft conflict resolution.  
It is part of the literature review for **Large Language Models for Aircraft Conflict Resolution**.  
All generated responses from this testing phase are also included.

---

## LLM Conflict Scenarios

All files related to conflict scenarios and conflicting aircraft are provided as JSON files.  
They can be accessed in two folders:  

- `aircraft_info_conf_2ac` – Aircraft information.  
- `confl_info_ac` – Conflict information.  

### Detecting Conflict

Results of the first set of experiments (**detecting_conflict**) can be found in subfolders within `LLM_responses`, organized by model name.  
Each model’s folder includes results for three test cases:

- **case_1** – Default prompt describing the conflict scenario.  
- **case_2** – Modified version of case_1 with latitude and longitude converted into Cartesian coordinates.  
- **case_3** – Conflict scenario enriched with exact details (e.g., TLOS) to evaluate model reasoning for conflict resolution commands.  

### Heading Change

The second set of experiments (**heading_change**) can be found in `LLM_responses` under the following model-specific folders:  

- `Gemini_2_5/heading_change`  
- `CHAT_GPT_4o/heading_change`  

---

## Scripts

Below is a brief explanation of the scripts included in this repository:

- **`LLM_model_config.py`** – Defines a dictionary of LLM models and their API connection settings.  
- **`LLM_reasoning.py`** – Sends prompts to the API and saves the model responses.  
- **`prompt_generator.py`** – Defines all prompts used for testing, including difficulty levels (case_1, case_2, case_3) for both conflict detection and heading change experiments.  
- **`saving_json_aircraft.py`** – Saves information on conflicting aircraft to create a JSON file once the BlueSky simulation is started.  
- **`saving_json_conflicts.py`** – Saves information on conflicts to create a JSON file once the BlueSky simulation is started.  

---













