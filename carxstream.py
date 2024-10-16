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
        'model': r'model:\s*([^\n,]+)',
        'variant': r'variant:\s*([^\n,]+)',
        'year': r'year:\s*(\d{4})',
        'price': r'price:\s*([\d,.]+)',
        'color': r'color:\s*([^\n,]+)',
        'number_plate': r'number plate:\s*([^\n,]+)',
        'odometer': r'odometer:\s*([\d,]+)',
        'fuel': r'fuel:\s*([^\n,]+)',
    }
    
    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            extracted_data[key] = match.group(1).strip()
    
    return extracted_data

def find_best_match(car_data: Dict[str, str], all_car_data: pd.DataFrame) -> Optional[pd.Series]:
    """
    Finds the best matching car in the dataset based on provided details.
    """
    make = car_data.get('make', '').lower()
    model = car_data.get('model', '').lower()
    
    if not make or not model:
        return None
    
    make_model = f"{make} {model}"
    all_car_data['match_score'] = all_car_data.apply(lambda row: fuzz.ratio(make_model, f"{row['Make']} {row['Model']}".lower()), axis=1)
    
    # Filter by year if provided
    if 'year' in car_data:
        year = int(car_data['year'])
        all_car_data = all_car_data[all_car_data['Year'] == year]
    
    # Additional filtering can be added here for other fields
    
    best_match = all_car_data.loc[all_car_data['match_score'].idxmax()]
    
    return best_match if best_match['match_score'] > 70 else None

def get_car_info(car_data: Dict[str, str], all_car_data: pd.DataFrame) -> str:
    """
    Processes car data and returns relevant information.
    """
    if not car_data.get('make') or not car_data.get('model'):
        return "Please provide at least the make and model of the car."
    
    best_match = find_best_match(car_data, all_car_data)
    
    if best_match is None:
        return f"Sorry, I couldn't find any information about the {car_data.get('make')} {car_data.get('model')}."
    
    response = f"The {best_match['Make']} {best_match['Model']} "
    
    if 'year' in car_data:
        response += f"from {car_data['year']} "
    
    # Add more details as available in your dataset and user input
    if 'Price' in best_match and pd.notna(best_match['Price']):
        response += f"has a price of approximately {best_match['Price']}. "
    elif 'price' in car_data:
        response += f"is priced at {car_data['price']}. "
    
    if 'Fuel Type' in best_match and pd.notna(best_match['Fuel Type']):
        response += f"It runs on {best_match['Fuel Type']}. "
    elif 'fuel' in car_data:
        response += f"It runs on {car_data['fuel']}. "
    
    # Add other details from user input
    for key in ['variant', 'color', 'number_plate', 'odometer']:
        if key in car_data:
            response += f"The {key.replace('_', ' ')} is {car_data[key]}. "
    
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
    st.write("Please provide car details in the following format:")
    st.write("Make: [Car Make]")
    st.write("Model: [Car Model]")
    st.write("Variant: [optional]")
    st.write("Year: [optional]")
    st.write("Price: [optional]")
    st.write("Color: [optional]")
    st.write("Number Plate: [optional]")
    st.write("Odometer: [optional]")
    st.write("Fuel: [optional]")

    user_input = st.text_area("Ask me about a car (e.g., 'Ford Aspire 2018'):")

    if user_input:
        response = process_user_query(user_input, all_car_data)
        st.write(response)

if __name__ == "__main__":
    main()