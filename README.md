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



### Case 3
| file                | chat gpt-4o command                                                                 | deepseek command                                                                 | gemini-2.5 command                                                                                                   | llama-70b command                                                                                                             | sonnet-3.7 command                                                                                                                                   |
|---------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2ac_converging_dh_1 | FLIGHT1, turn right heading 340 degrees and reduce speed to 220 knots. FLIGHT2, stop descent and maintain flight level 190, turn left heading 290 degrees. | FLIGHT2, descend and level off at 19,093 feet. FLIGHT2, turn right to a heading of 330 degrees. FLIGHT1, maintain current altitude and heading. FLIGHT2, reduce speed to 237 knots. | FLIGHT1, descend maintain Flight Level One Seven Zero.                                                                | FLIGHT2: Climb and maintain 20000 feet, FLIGHT1: Turn right heading 340 degrees, FLIGHT2: Reduce speed to 250 knots           | FLIGHT2: Turn left heading 290 degrees and maintain FL190. FLIGHT1: Descend and maintain FL170.                                                    |
| 2ac_converging_dh_2 | FLIGHT2, stop descent and maintain 18,500 feet; FLIGHT1, turn right heading 330 degrees; FLIGHT2, reduce speed to 250 knots. | FLIGHT1: Turn right heading 350°, FLIGHT2: Reduce speed to 260 knots             | FLIGHT2, stop descent immediately, maintain Flight Level One Eight Zero. FLIGHT1, turn right heading Three Six Zero. | FLIGHT2: Climb and maintain 19000 feet, turn right heading 320 degrees, and reduce speed to 250 knots                         | FLIGHT2, Traffic Alert. Stop descent immediately, maintain FL180. FLIGHT2, for traffic separation, turn right heading 330 degrees.                  |
| 2ac_head_1          | FLIGHT1, climb to 16,500 feet and adjust heading to 130 degrees. FLIGHT2, maintain current altitude and adjust heading to 310 degrees. | FLIGHT1: Turn right heading 160 degrees, FLIGHT2: Turn left heading 340 degrees. Alternatively, FLIGHT1: Reduce speed to 230 knots, FLIGHT2: Increase speed to 250 knots | Turn FLIGHT1 right heading 170, turn FLIGHT2 right heading 350 immediately for traffic avoidance.                   | FLIGHT1, turn right heading 160 degrees, reduce speed to 240 knots.                                                           |                                                                                                                                                      |
| 2ac_head_2          | FLIGHT1, turn left heading 120 degrees. FLIGHT1, reduce speed to 270 knots. FLIGHT2, maintain current altitude, stop descent. | FLIGHT1: Turn right heading 160 degrees, reduce ground speed to 280 knots. FLIGHT2: Descend to 17,000 feet. | FLIGHT2, MAINTAIN FLIGHT LEVEL ONE EIGHT ZERO.                                                                        | FLIGHT1: Turn right heading 160 degrees, reduce ground speed to 250 knots. FLIGHT2: Descend to 17000 feet.                    | FLIGHT2, Traffic alert. For separation, turn right heading 350 degrees immediately.                                                               |
| 2ac_parallel_1      | FLIGHT1 to turn right by 10 degrees to a heading of 226 degrees; FLIGHT2 to turn left by 5 degrees to a heading of 211 degrees. | FLIGHT2, reduce speed to 280 knots and/or turn right heading 240 degrees         | FLIGHT2, descend and maintain Flight Level Two Four Zero.                                                             | FLIGHT2, climb and maintain 26,000 feet. Report level.                                                                        | FLIGHT1: Descend to FL240. FLIGHT2: Turn right heading 230 degrees.                                                                                 |
| 2ac_parallel_2      | Instruct FLIGHT1 to climb to 24,500 feet and adjust heading to 220 degrees. Instruct FLIGHT2 to maintain or increase its descent rate. | FLIGHT2, climb and maintain 25,000 feet. FLIGHT1, turn right heading 240 degrees. FLIGHT2, reduce ground speed to 300 knots. | FLIGHT2, TURN RIGHT HEADING 240, MAINTAIN FLIGHT LEVEL 240.                                                           | FLIGHT2: Climb to 25,000 feet at 500 feet/min and turn right heading 240 degrees. FLIGHT1: Maintain current heading and altitude. | FLIGHT2 instructed to stop descent and maintain FL242. FLIGHT1 instructed to turn right heading 240 degrees.                                       |
| 2ac_t_formation_1   | FLIGHT1, climb and maintain 21,000 feet. FLIGHT2, turn left heading 140 degrees.     | FLIGHT1, turn right heading 095 degrees. FLIGHT2, reduce speed to 370 knots.     | FLIGHT2, climb and maintain Flight Level Two Two Zero.                                                                | Heading change to FLIGHT1 to turn right by 20-30 degrees and consider speed reduction to FLIGHT2                               |                                                                                                                                                      |
| 2ac_t_formation_2   | FLIGHT1, climb immediately to 21000 feet and turn left heading 050 degrees. FLIGHT2, expedite descent to 20000 feet and turn right heading 180 degrees. | FLIGHT2, reduce speed to 280 knots. Report passing 22,000 feet.                  | FLIGHT2, stop descent IMMEDIATELY, maintain Flight Level 220. Turn right heading 190.                                 | FLIGHT2: Reduce ground speed to 280 knots and level off at current altitude (22,290 feet)                                      | FLIGHT2, traffic alert. Turn right heading 190 degrees immediately for traffic separation. Maintain current descent rate. Report new heading established. |













