import os
from io import BytesIO
import wolframalpha
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def get_nutrient_value(text_list, nutrient_name):
    """
    Helper function to extract nutrient value from the list of words.
    Searches for the nutrient name and extracts the value and unit following it.
    """
    try:
        # Find the index of the nutrient name
        index = -1
        for i, word in enumerate(text_list):
            if word == nutrient_name:
                index = i
                break
        
        if index == -1:
            return None

        value = text_list[index + 1]
        unit = text_list[index + 2]
        
        # Basic cleaning of value (remove non-numeric chars if any, though int() handles clean strings)
        # Assuming value is a clean integer string based on previous code logic
        numeric_value = int(value)

        if unit == 'g':
            return numeric_value * 1000
        elif unit == 'μg':
            return numeric_value / 1000
        else:
            return numeric_value
    except (ValueError, IndexError) as e:
        print(f"Error extracting {nutrient_name}: {e}")
        return 0

def nutrients(food): 
    food = food + " nutritional info"
    app_id = os.getenv('WOLFRAM_APP_ID')
    if not app_id:
        print("Error: WOLFRAM_APP_ID not found in environment variables.")
        return [{}, ""]

    client = wolframalpha.Client(app_id)
    try:
        res = client.query(food)
        # Check if 'pod' exists in response to avoid errors if query fails
        if not hasattr(res, 'pod'):
             print("No results found from WolframAlpha")
             return [{}, ""]
             
        url = res.pod[1].subpod.img.src
        # print(url)
        
        # Only fetch image if needed, but the original code returns it (or url)
        # response = requests.get(url)
        # img = Image.open(BytesIO(response.content))

        ans = next(res.results).text
        li = list(ans.split(" "))
        print(li)
        
        nutrients_data = {}
        
        # Extract nutrients using the helper function
        # Note: The original code had specific start indices (li[10:], li[20:] etc.) 
        # which suggests the output format is very specific. 
        # However, searching the whole list is generally safer if the order changes slightly 
        # but the structure remains similar. 
        # If the specific offsets were critical to avoid false matches, this might need adjustment.
        # For now, I will search the entire list as it's more robust to slight shifts.
        
        nutrients_data['fat'] = get_nutrient_value(li, 'fat') or 0
        nutrients_data['carbohydrates'] = get_nutrient_value(li, 'carbohydrates') or 0
        nutrients_data['cholesterol'] = get_nutrient_value(li, 'cholesterol') or 0
        nutrients_data['protein'] = get_nutrient_value(li, 'protein') or 0
        nutrients_data['sodium'] = get_nutrient_value(li, 'sodium') or 0

        print(nutrients_data)
        return [nutrients_data, url]

    except Exception as e:
        print(f"Error in nutrients function: {e}")
        return [{}, ""]

    # Image(url)
    # print(img)
    # return Image(url)
    # next(ans)
    
# nutrients("apple")