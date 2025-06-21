import json

def parse_json_string(json_string):
    """
    Parse a JSON string into a Python dictionary.
    
    Args:
        json_string (str): The JSON string to parse.
        
    Returns:
        dict: The parsed JSON as a dictionary, or an empty dictionary if parsing fails.
    """
    try:
        cleaned_string = json_string.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_string)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}