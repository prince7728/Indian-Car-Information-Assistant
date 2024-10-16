# import pandas as pd
# import re
# from fuzzywuzzy import fuzz
# from typing import Dict, List, Optional

# # Load the car dataset
# # Assuming the dataset is in CSV format. Adjust the path as necessary.
# df = pd.read_json('IndianCarMasterDataOutput.json')

# def preprocess_input(user_input: str) -> Dict[str, str]:
#     """
#     Extracts car details from user input using regex patterns.
#     """
#     patterns = {
#         'make': r'make:\s*(\w+)',
#         'model': r'model:\s*(\w+)',
#         'variant': r'variant:\s*(\w+)',
#         'year': r'year:\s*(\d{4})',
#         'price': r'price:\s*([\d.]+)',
#         'color': r'color:\s*(\w+)',
#         'number_plate': r'number plate:\s*(\w+)',
#         'odometer': r'odometer:\s*(\d+)',
#         'fuel': r'fuel:\s*(\w+)'
#     }
    
#     extracted_data = {}
#     for key, pattern in patterns.items():
#         match = re.search(pattern, user_input, re.IGNORECASE)
#         if match:
#             extracted_data[key] = match.group(1)
    
#     return extracted_data

# def find_best_match(make: str, model: str) -> Optional[pd.Series]:
#     """
#     Finds the best matching car in the dataset based on make and model.
#     """
#     make_model = f"{make} {model}".lower()
#     df['match_score'] = df.apply(lambda row: fuzz.ratio(make_model, f"{row['Make']} {row['Model']}".lower()), axis=1)
#     best_match = df.loc[df['match_score'].idxmax()]
    
#     return best_match if best_match['match_score'] > 70 else None

# def get_car_info(car_data: Dict[str, str]) -> str:
#     """
#     Processes car data and returns relevant information.
#     """
#     make = car_data.get('make')
#     model = car_data.get('model')
    
#     if not make or not model:
#         return "Please provide both the make and model of the car."
    
#     best_match = find_best_match(make, model)
    
#     if best_match is None:
#         return f"Sorry, I couldn't find any information about the {make} {model}."
    
#     response = f"The {best_match['Make']} {best_match['Model']} "
    
#     if 'year' in car_data:
#         response += f"from {car_data['year']} "
#     elif 'Year' in best_match:
#         response += f"is available in various years, including {best_match['Year']}. "
    
#     if 'Variant' in best_match:
#         response += f"comes in multiple variants, including {best_match['Variant']}. "
    
#     if 'Price' in best_match:
#         response += f"The average price is around ₹{best_match['Price']} lakhs. "
    
#     if 'Color' in best_match:
#         response += f"It's available in colors like {best_match['Color']}. "
    
#     if 'Fuel' in best_match:
#         response += f"It typically runs on {best_match['Fuel']}. "
    
#     if 'Odometer' in best_match:
#         response += f"The average mileage for this model is around {best_match['Odometer']} km. "
    
#     return response.strip()

# def process_user_query(user_input: str) -> str:
#     """
#     Processes a natural language query about a car.
#     """
#     car_data = preprocess_input(user_input)
#     return get_car_info(car_data)

# # Example usage
# if __name__ == "__main__":
#     while True:
#         user_input = input("Ask me about a car (or type 'quit' to exit): ")
#         if user_input.lower() == 'quit':
#             break
#         response = process_user_query(user_input)
#         print(response)
#         print()







# import json
# import re
# import pandas as pd
# from fuzzywuzzy import fuzz
# from typing import Dict, List, Optional

# def load_car_data(file_path: str) -> pd.DataFrame:
#     """
#     Load car data from a JSON file into a pandas DataFrame.
#     """
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     df = pd.DataFrame(data)
#     return df.dropna(subset=['Make', 'Model'])  # Remove rows with NaN Make or Model

# def preprocess_input(user_input: str) -> Dict[str, str]:
#     """
#     Extracts car details from user input using regex patterns.
#     """
#     patterns = {
#         'make': r'make:\s*(\w+)',
#         'model': r'model:\s*([^\d,]+)',
#         'year': r'year:\s*(\d{4})',
#     }
    
#     extracted_data = {}
#     for key, pattern in patterns.items():
#         match = re.search(pattern, user_input, re.IGNORECASE)
#         if match:
#             extracted_data[key] = match.group(1).strip()
    
#     return extracted_data

# def find_best_match(make: str, model: str, car_data: pd.DataFrame) -> Optional[pd.Series]:
#     """
#     Finds the best matching car in the dataset based on make and model.
#     """
#     make_model = f"{make} {model}".lower()
#     car_data['match_score'] = car_data.apply(lambda row: fuzz.ratio(make_model, f"{row['Make']} {row['Model']}".lower()), axis=1)
#     best_match = car_data.loc[car_data['match_score'].idxmax()]
    
#     return best_match if best_match['match_score'] > 70 else None

# def get_car_info(car_data: Dict[str, str], all_car_data: pd.DataFrame) -> str:
#     """
#     Processes car data and returns relevant information.
#     """
#     make = car_data.get('make')
#     model = car_data.get('model')
    
#     if not make or not model:
#         return "Please provide both the make and model of the car."
    
#     best_match = find_best_match(make, model, all_car_data)
    
#     if best_match is None:
#         return f"Sorry, I couldn't find any information about the {make} {model}."
    
#     response = f"The {best_match['Make']} {best_match['Model']} "
    
#     if 'year' in car_data:
#         response += f"from {car_data['year']} "
    
#     # Add more details as available in your dataset
#     if 'Price' in best_match and pd.notna(best_match['Price']):
#         response += f"has a price of approximately {best_match['Price']}. "
    
#     if 'Fuel Type' in best_match and pd.notna(best_match['Fuel Type']):
#         response += f"It runs on {best_match['Fuel Type']}. "
    
#     # Add more details as needed based on your dataset columns
    
#     return response.strip()

# def process_user_query(user_input: str, all_car_data: pd.DataFrame) -> str:
#     """
#     Processes a natural language query about a car.
#     """
#     car_data = preprocess_input(user_input)
    
#     # If no structured data was extracted, treat the entire input as potential make and model
#     if not car_data:
#         words = user_input.split()
#         if len(words) >= 2:
#             car_data['make'] = words[0]
#             car_data['model'] = ' '.join(words[1:])
#         elif len(words) == 1:
#             car_data['make'] = words[0]
    
#     if 'make' in car_data and 'model' not in car_data:
#         return f"You've mentioned the make as {car_data['make']}. Can you also provide the model?"
    
#     return get_car_info(car_data, all_car_data)

# def main():
#     print("Welcome to the Indian Car Information Assistant!")
#     print("Loading car data...")
#     all_car_data = load_car_data("IndianCarMasterDataOutput.json")
#     print(f"Loaded data for {len(all_car_data)} cars.")
    
#     # Debug: Print the first few entries in the dataset
#     print("Sample data:")
#     print(all_car_data[['Make', 'Model']].head())
    
#     print("\nYou can ask about a car by providing its make and model.")
#     print("For example: 'Ford Aspire' or 'Tell me about the Honda Amaze 2018'")
#     print("Type 'quit' to exit.")
#     print()

#     while True:
#         user_input = input("Ask me about a car: ")
#         if user_input.lower() == 'quit':
#             break
        
#         # Debug: Print the preprocessed input
#         car_data = preprocess_input(user_input)
#         print("Preprocessed input:", car_data)
        
#         response = process_user_query(user_input, all_car_data)
#         print(response)
#         print()

#     print("Thank you for using the Indian Car Information Assistant. Goodbye!")

# if __name__ == "__main__":
#     main()









import json
import re
import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st
from typing import Dict, List, Optional


# Load car data
@st.cache_data
def load_car_data(file_path: str) -> pd.DataFrame:
    """
    Load car data from a JSON file into a pandas DataFrame.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    return df.dropna(subset=['Make', 'Model'])  # Remove rows with NaN Make or Model

def preprocess_input(user_input: str) -> Dict[str, str]:
    """
    Extracts car details from user input using regex patterns.
    """
    patterns = {
        'make': r'make:\s*(\w+)',
        'model': r'model:\s*([^\d,]+)',
        'year': r'year:\s*(\d{4})',
    }
    
    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            extracted_data[key] = match.group(1).strip()
    
    return extracted_data

def find_best_match(make: str, model: str, car_data: pd.DataFrame) -> Optional[pd.Series]:
    """
    Finds the best matching car in the dataset based on make and model.
    """
    make_model = f"{make} {model}".lower()
    car_data['match_score'] = car_data.apply(lambda row: fuzz.ratio(make_model, f"{row['Make']} {row['Model']}".lower()), axis=1)
    best_match = car_data.loc[car_data['match_score'].idxmax()]
    
    return best_match if best_match['match_score'] > 70 else None

def get_car_info(car_data: Dict[str, str], all_car_data: pd.DataFrame) -> str:
    """
    Processes car data and returns relevant information.
    """
    make = car_data.get('make')
    model = car_data.get('model')
    
    if not make or not model:
        return "Please provide both the make and model of the car."
    
    best_match = find_best_match(make, model, all_car_data)
    
    if best_match is None:
        return f"Sorry, I couldn't find any information about the {make} {model}."
    
    response = f"The {best_match['Make']} {best_match['Model']} "
    
    if 'year' in car_data:
        response += f"from {car_data['year']} "
    
    # Add more details as available in your dataset
    if 'Price' in best_match and pd.notna(best_match['Price']):
        response += f"has a price of approximately {best_match['Price']}. "
    
    if 'Fuel Type' in best_match and pd.notna(best_match['Fuel Type']):
        response += f"It runs on {best_match['Fuel Type']}. "
    
    return response.strip()

def process_user_query(user_input: str, all_car_data: pd.DataFrame) -> str:
    """
    Processes a natural language query about a car.
    """
    car_data = preprocess_input(user_input)
    
    # If no structured data was extracted, treat the entire input as potential make and model
    if not car_data:
        words = user_input.split()
        if len(words) >= 2:
            car_data['make'] = words[0]
            car_data['model'] = ' '.join(words[1:])
        elif len(words) == 1:
            car_data['make'] = words[0]
    
    if 'make' in car_data and 'model' not in car_data:
        return f"You've mentioned the make as {car_data['make']}. Can you also provide the model?"
    
    return get_car_info(car_data, all_car_data)

# Streamlit App
def main():
    st.title("Indian Car Information Assistant")

    # Load car data
    all_car_data = load_car_data("IndianCarMasterDataOutput.json")
    
    st.write(f"Loaded data for {len(all_car_data)} cars.")

    # User input
    user_input = st.text_input("Ask me about a car (e.g., 'Ford Aspire 2018'):")

    if user_input:
        response = process_user_query(user_input, all_car_data)
        st.write(response)

if __name__ == "__main__":
    main()
