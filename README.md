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
- **`Min_head_change.py`** - Calculating the minimal heading change between 2 aircraft in conflict.
- **`Min_head_plot.py`** - Creating the plot for heading change experiment. 
---


## LMMs' Responses
### Case 1



| file                | chat gpt-4o command                                                                 | deepseek command                        | gemini-2.5 command                                                                 | llama-70b command                                                                 | sonnet-3.7 command                                                                                                                                                  |
|---------------------|--------------------------------------------------------------------------------------|------------------------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2ac_converging_dh_1 | -                                                                                    | -                                        | FLIGHT2, stop descent immediately, maintain flight level one niner zero.           | -                                                                                  | FLIGHT2, maintain FL190, stop descent.                                                                                                                             |
| 2ac_converging_dh_2 | FLIGHT2: Climb immediately to maintain 2000 feet separation.                         | -                                        | FLIGHT2, stop descent at Flight Level 170.                                         | -                                                                                  | FLIGHT2, maintain altitude at 18,000 feet, stop descent.                                                                                                           |
| 2ac_head_1          | FLIGHT1: Adjust heading to 130 degrees. FLIGHT2: Adjust heading to 310 degrees.      | -                                        | FLIGHT1, climb and maintain flight level one seven zero.                           | -                                                                                  | FLIGHT1, climb and maintain flight level 180. Traffic is FLIGHT2, a Boeing 777, at your 12 o'clock, 47 miles, opposite direction at flight level 162.              |
| 2ac_head_2          | -                                                                                    | -                                        | FLIGHT2, MAINTAIN ALTITUDE ONE EIGHT THOUSAND.                                     | -                                                                                  | FLIGHT2, maintain altitude at 18000 feet, stop descent.                                                                                                            |
| 2ac_parallel_1      | Instruct FLIGHT1 to change altitude to maintain vertical separation.                 | -                                        | -                                                                                  | -                                                                                  | -                                                                                                                                                                  |
| 2ac_parallel_2      | -                                                                                    | -                                        | -                                                                                  | Command FLIGHT2 to level off or climb to prevent reduction in vertical separation. | FLIGHT2, Air Traffic Control. To maintain separation, level off at flight level 240. Maintain current heading and speed. Acknowledge.                              |
| 2ac_t_formation_1   | Instruct FLIGHT1 to climb 1000 feet to maintain vertical separation.                  | -                                        | FLIGHT1, climb and maintain flight level two two zero.                             | -                                                                                  | FLIGHT1, for traffic separation, climb and maintain flight level 230. Report reaching.                                                                             |
| 2ac_t_formation_2   | -                                                                                    | FLIGHT2, descend and maintain 20000 feet. | FLIGHT2, level off immediately, maintain Flight Level Two Two Zero.                 | -                                                                                  | -                                                                                                                                                                  |


### Case 2
| file                | chat gpt-4o command                                                                 | deepseek command                                                                 | gemini-2.5 command                                                                 | llama-70b command                                                                 | sonnet-3.7 command                          |
|---------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------|
| 2ac_converging_dh_1 | -                                                                                    | -                                                                                | FLIGHT2, maintain one niner thousand.                                              | -                                                                                 | -                                           |
| 2ac_converging_dh_2 | -                                                                                    | -                                                                                | FLIGHT2, LEVEL OFF IMMEDIATELY, MAINTAIN FLIGHT LEVEL ONE EIGHT ZERO.              | -                                                                                 | -                                           |
| 2ac_head_1          | FLIGHT1: Change heading to 150 degrees to increase separation. FLIGHT2: Climb to 17200 feet to ensure vertical separation. | FLIGHT1, climb and maintain 17000 feet.                                          | FLIGHT1, climb immediately, maintain flight level one seven zero.                  | -                                                                                 | -                                           |
| 2ac_head_2          | FLIGHT2, climb and maintain 18500 feet.                                              | -                                                                                | FLIGHT2, maintain altitude one eight thousand.                                     | -                                                                                 | -                                           |
| 2ac_parallel_1      | -                                                                                    | Consider instructing FLIGHT2 to reduce its speed to match or come closer to FLIGHT1's speed. | FLIGHT2, climb and maintain Flight Level 260.                                      | Instruct FLIGHT2 to climb to 26200 feet to ensure a vertical separation of at least 1000 feet. | -                                           |
| 2ac_parallel_2      | -                                                                                    | -                                                                                | FLIGHT2, maintain present altitude.                                                | Consider commanding FLIGHT2 to level off or ascend to maintain or increase the vertical separation. | FLIGHT2, maintain flight level 240, cancel descent. |
| 2ac_t_formation_1   | -                                                                                    | -                                                                                | FLIGHT1, descend and maintain Flight Level Two Zero Zero.                          | FLIGHT1, turn right heading 090 degrees to increase separation with FLIGHT2, or FLIGHT2, climb and maintain 21000 feet to increase vertical separation with FLIGHT1. | -                                           |
| 2ac_t_formation_2   | -                                                                                    | -                                                                                | FLIGHT2, MAINTAIN FLIGHT LEVEL TWO TWO ZERO.                                       | -                                                                                 | -                                           |
















