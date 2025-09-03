#A file with prompt generation for specific level of difficulties
import pyproj


#---------------------------LEVEL 1-----------------------------------
def gen_prompt_lvl_1(aircraft_data, conflict_data):
    # Format the information into a readable text for LLM
    def format_aircraft_info(aircraft):
        return (f"Aircraft {aircraft['callsign']} ({aircraft['typecode']}) is at latitude {aircraft['latitude']}, "
                f"longitude {aircraft['longitude']}, flying at {aircraft['altitude (feet)']} feet. "
                f"Ground speed: {aircraft['groundspeed (knots)']} knots, heading: {aircraft['heading (degrees)']} degrees, "
                f"vertical rate: {aircraft['vertical_rate (feet/minute)']} feet/min.")


    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    #Combine the aircraft data prompt with the task and generate reasoning prompt
    reasoning_prompt = (
    "You are an air traffic controller. Based on the following data, determine if any aircraft "
    "pair will reach loss of seperation. Loss of separation occurs only when both conditions are met at the same time:\n"
    "- Vertical distance < 1000 feet\n"
    "- Horizontal distance < 5 nautical miles\n\n"
    f"{aircraft_summaries}\n\n"
    "Determine if there will be a loss of seperation and its possible time by providing step-by-step reasoning and by performing all calculations if necessary."
    )

    question = (
        "Based on the provided air traffic data, determine the necessary command(s) that should be issued "
        "to any aircraft to maintain safe separation, such as altitude adjustments, heading changes, or speed modifications."
    )

    reasoning_prompt = reasoning_prompt + question

    return reasoning_prompt 

#---------------------------LEVEL 2-----------------------------------


def lat_lon_to_utm(latitude, longitude):
    # Automatically determine the UTM zone based on longitude
    # UTM zones are based on longitude, with each zone spanning 6 degrees of longitude
    zone_number = int((longitude + 180) / 6) + 1
    
    # Define the UTM projection for the calculated zone
    utm_crs = pyproj.CRS(f"EPSG:326{zone_number:02d}")  # UTM zone for the Northern Hemisphere
    if latitude < 0:
        utm_crs = pyproj.CRS(f"EPSG:327{zone_number:02d}")  # UTM zone for the Southern Hemisphere
    
    # Create a transformer for the conversion from WGS84 (Lat/Lon) to UTM
    crs_wgs84 = pyproj.CRS("EPSG:4326")  # WGS84 (Lat/Lon)
    transformer = pyproj.Transformer.from_crs(crs_wgs84, utm_crs, always_xy=True)
    
    # Perform the conversion to UTM (meters)
    x, y = transformer.transform(longitude, latitude)
    
    return x, y

def gen_prompt_lvl_2(aircraft_data, conflict_data):

    # Format the information into a readable text for LLM
    def format_aircraft_info(aircraft):

        x_coordinate, y_coordinate = lat_lon_to_utm(aircraft['latitude'], aircraft['longitude'])

        return (f"Aircraft {aircraft['callsign']} ({aircraft['typecode']}) is at y coordinate {y_coordinate} meters, "
                f"x coordinate {x_coordinate} meters, flying at {aircraft['altitude (feet)']} feet. "
                f"Ground speed: {aircraft['groundspeed (knots)']} knots, heading: {aircraft['heading (degrees)']} degrees, "
                f"vertical rate: {aircraft['vertical_rate (feet/minute)']} feet/min.")


    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    #Combine the aircraft data prompt with the task and generate reasoning prompt
    reasoning_prompt = (
    "You are an air traffic controller. Based on the following data, determine if any aircraft "
    "pair will reach loss of seperation. Loss of separation occurs only when both conditions are met at the same time:\n"
    "- Vertical distance < 1000 feet\n"
    "- Horizontal distance < 5 nautical miles\n\n"
    f"{aircraft_summaries}\n\n"
    "Determine if there will be a loss of seperation and its possible time by providing step-by-step reasoning and by performing all calculations if necessary."
    )

    question = (
        "Based on the provided air traffic data, determine the necessary command(s) that should be issued "
        "to any aircraft to maintain safe separation, such as altitude adjustments, heading changes, or speed modifications."
    )

    reasoning_prompt = reasoning_prompt + question

    return reasoning_prompt

# ---------------------------LEVEL 3-----------------------------------

def gen_prompt_lvl_3(aircraft_data, conflict_data):

    # Format the information into a readable text for LLM
    def format_aircraft_info(aircraft):

        # Ensure lat_lon_to_utm function exists
        x_coordinate, y_coordinate = lat_lon_to_utm(aircraft['latitude'], aircraft['longitude'])

        return (f"Aircraft {aircraft['callsign']} ({aircraft['typecode']}) is at y coordinate {y_coordinate} meters, "
                f"x coordinate {x_coordinate} meters, flying at {aircraft['altitude (feet)']} feet. "
                f"Ground speed: {aircraft['groundspeed (knots)']} knots, heading: {aircraft['heading (degrees)']} degrees, "
                f"vertical rate: {aircraft['vertical_rate (feet/minute)']} feet/min.")
    
    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    intro_prompt = "You are an air traffic controller with the following data available where a loss of separation has been detected.\n\n"

    # Fixing `conflict_prompt` formatting issue
    conflict_prompt = (
        f"A conflict has been detected between Aircraft {conflict_data[0]['conflict pairs'][0]} "
        f"and Aircraft {conflict_data[0]['conflict pairs'][1]}. "
        f"The current horizontal distance between them is {conflict_data[0]['distance (nautical miles)']:.2f} nautical miles, "
        f"with an altitude difference of {conflict_data[0]['altitude difference (feet)']:.1f} feet. "
        f"The azimuthal direction (QDR) from {conflict_data[0]['conflict pairs'][0]} to "
        f"{conflict_data[0]['conflict pairs'][1]} is {conflict_data[0]['qdr (degrees)']:.2f} degrees.\n\n"
        
        f"The estimated time to loss of separation (TLOS) is {conflict_data[0]['tlos (seconds)']:.1f} seconds, "
        f"indicating when the aircraft may violate the minimum separation criteria. "
        f"The predicted closest point of approach (DCPA) is {conflict_data[0]['dcpa (meters)']:.2f} meters, "
        f"expected to occur in {conflict_data[0]['tcpa (seconds)']:.1f} seconds.\n\n"
    )

    question = (
        "Based on the provided air traffic data, determine the necessary command(s) that should be issued "
        "to any aircraft to maintain safe separation, such as altitude adjustments, heading changes, or speed modifications."
    )

    # Proper concatenation
    reasoning_prompt = intro_prompt + aircraft_summaries + "\n\n" + conflict_prompt + question

    return reasoning_prompt

# ---------------------------LEVEL 4-----------------------------------

def gen_prompt_lvl_4(aircraft_data, conflict_data):

    # Format the information into a readable text for LLM
    def format_aircraft_info(aircraft):

        x_coordinate, y_coordinate = lat_lon_to_utm(aircraft['latitude'], aircraft['longitude'])

        return (f"Aircraft {aircraft['callsign']} ({aircraft['typecode']}) is at y coordinate {y_coordinate} meters, "
                f"x coordinate {x_coordinate} meters, flying at {aircraft['altitude (feet)']} feet. "
                f"Ground speed: {aircraft['groundspeed (knots)']} knots, heading: {aircraft['heading (degrees)']} degrees, "
                f"vertical rate: {aircraft['vertical_rate (feet/minute)']} feet/min.")


    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    #Combine the aircraft data prompt with the task and generate reasoning prompt
    reasoning_prompt = (
    "You are an air traffic controller. Based on the following data, determine if any aircraft "
    "pair will reach loss of seperation. Loss of separation occurs only when both conditions are met at the same time:\n"
    "- Vertical distance < 1000 feet\n"
    "- Horizontal distance < 5 nautical miles\n\n"
    f"{aircraft_summaries}\n\n"
    "Follow this step-by-step reasoning and perform all necessary calculations. The step-by-step reasoning:\n" 
    "1. Define Loss of Separation Criteria. \n"
    "2. Convert Current Units to Standard Units.\n"
    "3. Calculate Initial Separation (t = 0) using current positions and altitudes. Vertical Separation = |Altitude2 - Altitude1| and for Horizontal Separation compute Δx, Δy and Horizontal_Distance = sqrt(Δx² + Δy²).Assess whether LoS exists at time t = 0.\n"
    "4. Predict Aircraft Trajectories Over Time. Calculate components of velocity for each: vx = speed * sin(θ), vy = speed * cos(θ). Define position as a function of time t where x1(t) = x1_initial + vx1 * t, y1(t) = y1_initial + vy1 * t, x2(t) = x2_initial + vx2 * t, y2(t) = y2_initial + vy2 * t \n"
    "5.  Analyze Separation Over Time. Vertical Separation V(t): V(t) = |Alt2(t) - Alt1(t)| and solve for V(t) < critical Vertical distance. Horizontal Separation H(t): Δx(t) = x2(t) - x1(t), Δy(t) = y2(t) - y1(t) and H(t)² = Δx(t)² + Δy(t)² and Solve for H(t) < critical horizontal distance. \n"
    "6.  Identify Simultaneous LoS. Compare the time intervals. Find the overlap of Time interval when vertical separation is < critical Vertical distance, and Time interval of horizontal separation when it is < critical Horizontal distance.\n"
    )

    question = (
        "Based on the provided air traffic data and your analysis, determine the necessary command(s) that should be issued "
        "to any aircraft to maintain safe separation, such as altitude adjustments, heading changes, or speed modifications."
    )

    reasoning_prompt = reasoning_prompt + question

    return reasoning_prompt

# ---------------------------LEVEL 5-----------------------------------
def gen_prompt_lvl_5(aircraft_data, conflict_data):

    # Format the information into a readable text for LLM
    def format_aircraft_info(aircraft):

        # Ensure lat_lon_to_utm function exists
        x_coordinate, y_coordinate = lat_lon_to_utm(aircraft['latitude'], aircraft['longitude'])

        return (f"Aircraft {aircraft['callsign']} ({aircraft['typecode']}) is at y coordinate {y_coordinate} meters, "
                f"x coordinate {x_coordinate} meters, flying at {aircraft['altitude (feet)']} feet. "
                f"Ground speed: {aircraft['groundspeed (knots)']} knots, heading: {aircraft['heading (degrees)']} degrees, "
                f"vertical rate: {aircraft['vertical_rate (feet/minute)']} feet/min.")
    
    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    intro_prompt = "You are an air traffic controller with the following data available where a loss of separation has been detected.\n\n"

    # Fixing `conflict_prompt` formatting issue
    conflict_prompt = (
        f"A conflict has been detected between Aircraft {conflict_data[0]['conflict pairs'][0]} "
        f"and Aircraft {conflict_data[0]['conflict pairs'][1]}. "
        f"The current horizontal distance between them is {conflict_data[0]['distance (nautical miles)']:.2f} nautical miles, "
        f"with an altitude difference of {conflict_data[0]['altitude difference (feet)']:.1f} feet. "
        f"The azimuthal direction (QDR) from {conflict_data[0]['conflict pairs'][0]} to "
        f"{conflict_data[0]['conflict pairs'][1]} is {conflict_data[0]['qdr (degrees)']:.2f} degrees.\n\n"
        
        f"The estimated time to loss of separation (TLOS) is {conflict_data[0]['tlos (seconds)']:.1f} seconds, "
        f"indicating when the aircraft may violate the minimum separation criteria. "
        f"The predicted closest point of approach (DCPA) is {conflict_data[0]['dcpa (meters)']:.2f} meters, "
        f"expected to occur in {conflict_data[0]['tcpa (seconds)']:.1f} seconds.\n\n"
    )

    question = (
                "Based on the provided air traffic data, determine the most optimized command(s) "
                "that should be issued to any aircraft to maintain safe separation, prioritizing the least number of necessary actions (like changes of speed, altitude, heading) while still ensuring the conflict is safely and effectively avoided. "
                "Provide rationale for your chosen command."
    )

    # Proper concatenation
    reasoning_prompt = intro_prompt + aircraft_summaries + "\n\n" + conflict_prompt + question

    return reasoning_prompt

# ---------------------------LEVEL 6-----------------------------------
def gen_prompt_lvl_6(aircraft_data, conflict_data):

    # Format the information into a readable text for LLM
    def format_aircraft_info(aircraft):

        # Ensure lat_lon_to_utm function exists
        x_coordinate, y_coordinate = lat_lon_to_utm(aircraft['latitude'], aircraft['longitude'])

        return (f"Aircraft {aircraft['callsign']} ({aircraft['typecode']}) is at y coordinate {y_coordinate} meters, "
                f"x coordinate {x_coordinate} meters, flying at {aircraft['altitude (feet)']} feet. "
                f"Ground speed: {aircraft['groundspeed (knots)']} knots, heading: {aircraft['heading (degrees)']} degrees, "
                f"vertical rate: {aircraft['vertical_rate (feet/minute)']} feet/min.")
    
    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    intro_prompt = "You are an air traffic controller with the following data available where a loss of separation has been detected.\n\n"

    # Fixing `conflict_prompt` formatting issue
    conflict_prompt = (
        f"A conflict has been detected between Aircraft {conflict_data[0]['conflict pairs'][0]} "
        f"and Aircraft {conflict_data[0]['conflict pairs'][1]}. "
        f"The current horizontal distance between them is {conflict_data[0]['distance (nautical miles)']:.2f} nautical miles, "
        f"with an altitude difference of {conflict_data[0]['altitude difference (feet)']:.1f} feet. "
        f"The azimuthal direction (QDR) from {conflict_data[0]['conflict pairs'][0]} to "
        f"{conflict_data[0]['conflict pairs'][1]} is {conflict_data[0]['qdr (degrees)']:.2f} degrees.\n\n"
        
        f"The estimated time to loss of separation (TLOS) is {conflict_data[0]['tlos (seconds)']:.1f} seconds, "
        f"indicating when the aircraft may violate the minimum separation criteria. "
        f"The predicted closest point of approach (DCPA) is {conflict_data[0]['dcpa (meters)']:.2f} meters, "
        f"expected to occur in {conflict_data[0]['tcpa (seconds)']:.1f} seconds.\n\n"
    )

    question = (" Loss of separation occurs only when both conditions are met at the same time:\n"
                "- Vertical distance < 1000 feet\n"
                "- Horizontal distance < 5 nautical miles\n\n"
                "Based on the provided air traffic data, determine the most optimized command(s) "
                "that should be issued to any aircraft to maintain safe separation, prioritizing the least number of necessary actions (like changes of speed, altitude, heading) while still ensuring the conflict is safely and effectively avoided. "
                "Provide rationale for your chosen command."
    )

    # Proper concatenation
    reasoning_prompt = intro_prompt + aircraft_summaries + "\n\n" + conflict_prompt + question

    return reasoning_prompt

#-----------------JSON PROMPT GENERATOR-------
def gen_json_prompt(reasoning_text):

    json_prompt = json_prompt = f"""
    Based on the following reasoning, provide only a VALID JSON response describing if there is a loss of separation.

    Reasoning:
    {reasoning_text}

    The JSON format should look like:
    {{
    "conflict_detected": true/false,
    "conflicting_pairs": [
        {{
        "aircraft_1": "CALLSIGN_1",
        "aircraft_2": "CALLSIGN_2",
        "time_to_conflict_seconds": TIME_VALUE,
        "reasoning": "Short explanation"
        "issued command" : "command issued to avoid loss of seperation"
        }}
    ]
    }}

    If there is no conflict, return:
    {{ "conflict_detected": false, "message": "No conflicts detected." }}
    """
    return json_prompt
#################################################################################################
def gen_prompt_conflict(conflict_data):
    # Fixing `conflict_prompt` formatting issue
    conflict_prompt = (
        f"A conflict has been detected between Aircraft {conflict_data[0]['conflict pairs'][0]} "
        f"and Aircraft {conflict_data[0]['conflict pairs'][1]}. "
        f"The current horizontal distance between them is {conflict_data[0]['distance (nautical miles)']:.2f} nautical miles, "
        f"with an altitude difference of {conflict_data[0]['altitude difference (feet)']:.1f} feet. "
        f"The azimuthal direction (QDR) from {conflict_data[0]['conflict pairs'][0]} to "
        f"{conflict_data[0]['conflict pairs'][1]} is {conflict_data[0]['qdr (degrees)']:.2f} degrees.\n\n"
        
        f"The estimated time to loss of separation (TLOS) is {conflict_data[0]['tlos (seconds)']:.1f} seconds, "
        f"indicating when the aircraft may violate the minimum separation criteria. "
        f"The predicted closest point of approach (DCPA) is {conflict_data[0]['dcpa (meters)']:.2f} meters, "
        f"expected to occur in {conflict_data[0]['tcpa (seconds)']:.1f} seconds.\n\n"
    )
    return conflict_prompt

# Format the information into a readable text for LLM
def format_aircraft_info(aircraft):

    # Ensure lat_lon_to_utm function exists
    x_coordinate, y_coordinate = lat_lon_to_utm(aircraft['latitude'], aircraft['longitude'])

    return (f"Aircraft {aircraft['callsign']} ({aircraft['typecode']}) is at y coordinate {y_coordinate} meters, "
            f"x coordinate {x_coordinate} meters, flying at {aircraft['altitude (feet)']} feet. "
            f"Ground speed (TAS): {aircraft['groundspeed (knots)']} knots, CAS speed: {aircraft['CAS (knots)']} knots, heading: {aircraft['heading (degrees)']} degrees, "
            f"vertical rate: {aircraft['vertical_rate (feet/minute)']} feet/min.")

# ---------------------------HEAD_EXP-----------------------------------
def gen_prompt_lvl_head_exp(aircraft_data, conflict_data):

    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    intro_prompt = "You are an air traffic controller with the following data available where a loss of separation has been detected.\n\n"

    # Fixing `conflict_prompt` formatting issue
    conflict_prompt = gen_prompt_conflict(conflict_data)

    question = (" Loss of separation occurs only when both conditions are met at the same time:\n"
                "- Vertical distance < 1000 feet\n"
                "- Horizontal distance < 5 nautical miles\n\n"
                f"Based on the provided air traffic data, Solve the conflict only by changing heading of {conflict_data[0]['conflict pairs'][0]} in the optimal way while not violating minimum loss of seperation criteria"
                "Provide rationale for your chosen command."
    )

    # Proper concatenation
    reasoning_prompt = intro_prompt + aircraft_summaries + "\n\n" + conflict_prompt + question

    return reasoning_prompt

#-----------------  HEAD_EXP JSON PROMPT GENERATOR-------
def gen_json_prompt_head_exp(reasoning_text, aircraft_data, conflict_data):

    conflict_prompt = gen_prompt_conflict(conflict_data)
    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])
    json_prompt = json_prompt = f"""
    Based on the following data and reasoning_text, provide only a VALID JSON response regarding the conflict resolution.
    
    Aircraft summary:
    {aircraft_summaries}

    Conflict data: 
    {conflict_prompt}
    
    Reasoning:
    {reasoning_text}

    The JSON format should look like:
    {{
    "conflict_detected": true/false,
    "conflicting_pairs": [
        {{
        "aircraft_1": "CALLSIGN_1",
        "aircraft_2": "CALLSIGN_2",
        "time_to_conflict": TIME in seconds to the loss of seperation.
        "FLIGHT_1_CAS": CAS speed in knots of FLIGHT_1
        "FLIGHT_1_TAS": TAS speed in knots of FLIGHT_1
        "issued_command" : command issued to avoid loss of seperation. If conflict was unavoidable input "None".
        "heading_change" : the issued heading change in degrees to avoid conflict. If conflict was unavoidable input "None".
        "new_heading_FLIGHT1" : the new heading after applying the issued command. If conflict was unavoidable input "None".
        "reasoning": Short explanation for the command choice
        }}
    ]
    }}

    """
    return json_prompt

# ---------------------------HEAD_EXP_free_choice-----------------------------------
def gen_prompt_lvl_head_exp_free_choice(aircraft_data, conflict_data):

    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])

    intro_prompt = "You are an air traffic controller with the following data available where a loss of separation has been detected.\n\n"

    # Fixing `conflict_prompt` formatting issue
    conflict_prompt = gen_prompt_conflict(conflict_data)

    question = (" Loss of separation occurs only when both conditions are met at the same time:\n"
                "- Vertical distance < 1000 feet\n"
                "- Horizontal distance < 5 nautical miles\n\n"
                f"Based on the provided air traffic data, Solve the conflict only by adapting {conflict_data[0]['conflict pairs'][0]} flightpath in the optimal way while not violating minimum loss of seperation criteria. You can change heading angle, altitude, speed or a combination of these."
                "Provide rationale for your chosen command."
    )

    # Proper concatenation
    reasoning_prompt = intro_prompt + aircraft_summaries + "\n\n" + conflict_prompt + question

    return reasoning_prompt

#-----------------  HEAD_EXP_free_choice JSON PROMPT GENERATOR-------
def gen_json_prompt_head_exp_free_choice(reasoning_text, aircraft_data, conflict_data):

    conflict_prompt = gen_prompt_conflict(conflict_data)
    # Convert all aircraft data into formatted text
    aircraft_summaries = "\n".join([format_aircraft_info(ac) for ac in aircraft_data])
    json_prompt = json_prompt = f"""
    Based on the following data and reasoning_text, provide only a VALID JSON response regarding the conflict resolution.
    
    Aircraft summary:
    {aircraft_summaries}

    Conflict data: 
    {conflict_prompt}
    
    Reasoning:
    {reasoning_text}

    The JSON format should look like:
    {{
    "conflict_detected": true/false,
    "conflicting_pairs": [
        {{
        "aircraft_1": "CALLSIGN_1",
        "aircraft_2": "CALLSIGN_2",
        "time_to_conflict": TIME in seconds to the loss of seperation.
        "FLIGHT_1_CAS": CAS speed in knots of FLIGHT_1
        "FLIGHT_1_TAS": TAS speed in knots of FLIGHT_1
        "change of heading:" Was the heading chnaged? true/false
        "change of altitude:" Was the altitude chnaged? true/false
        "change of speed:" Was the speed chnaged? true/false
        "issued_command" : command issued to avoid loss of seperation. If conflict was unavoidable input "None".
        "heading_change" : the issued heading change in degrees to avoid conflict. If conflict was unavoidable input "None".
        "new_heading_FLIGHT1" : the new heading after applying the issued command. If conflict was unavoidable input "None".
        "reasoning": Short explanation for the command choice
        }}
    ]
    }}

    """
    return json_prompt
    
#DEF dictionnary
# Dictionary to map difficulty levels to functions
prompt_fun_dict = {
    1: gen_prompt_lvl_1,
    2: gen_prompt_lvl_2,
    3: gen_prompt_lvl_3,
    4: gen_prompt_lvl_4,
    5: gen_prompt_lvl_5,
    6: gen_prompt_lvl_6,
    "Head_exp" : gen_prompt_lvl_head_exp,
    "Head_exp_json":gen_json_prompt_head_exp,
    "Head_exp_free_choice" :gen_prompt_lvl_head_exp_free_choice,
    "Head_exp_json_free_choice": gen_json_prompt_head_exp_free_choice
}