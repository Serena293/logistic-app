from flask import Flask
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# create absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
rules_path = os.path.join(current_dir, "rules.json")

# open json file and save into a dictionary
with open(rules_path, "r", encoding="utf-8") as jsonfile:
    data = json.load(jsonfile)

def calculate_volume_cm3(length_cm, width_cm, height_cm):
    """
    Calculate the volume of a package in cubic centimeters.
    
    Args:
        length_cm (float): Length in centimeters
        width_cm (float): Width in centimeters  
        height_cm (float): Height in centimeters
        
    Returns:
        float: Volume in cubic centimeters (cm³)
    """
    # Convert inputs to float to handle both int and string inputs
    length = float(length_cm)
    width = float(width_cm)
    height = float(height_cm)
    
    # Calculate volume: length × width × height
    volume = length * width * height
    
    return volume


def calculate_shipping_price(params, pricing_rules):
    """
    Calculate total shipping price based on package parameters and pricing rules.
    
    Args:
        params (dict): Package parameters from frontend:
            - length_cm (float): Length in cm
            - width_cm (float): Width in cm
            - height_cm (float): Height in cm
            - weight_kg (float): Weight in kg
            - is_express (bool): True for express shipping
            - destination (str): 'national' or 'international'
        pricing_rules (dict): Pricing rules from rules.json
        
    Returns:
        float: Total price in EUR
    """
    # Extract parameters with defaults
    length = float(params.get('length_cm', 0))
    width = float(params.get('width_cm', 0))
    height = float(params.get('height_cm', 0))
    weight = float(params.get('weight_kg', 0))
    is_express = bool(params.get('is_express', False))
    destination = params.get('destination', 'national')
    
    #validation
    if any(float(params.get(key, 0)) < 0 for key in ['length_cm', 'width_cm', 'height_cm', 'weight_kg']):
        raise ValueError("Values can not be negative number")
    if not params or not isinstance(params, dict):
        raise ValueError("Params must be a non-empty dictionary")
    # Calculate volume
    volume = calculate_volume_cm3(length, width, height)
    
    # Start with base price
    total = pricing_rules['base_price']
    
    # Add weight cost: price_per_kg × weight
    total += pricing_rules['price_per_kg'] * weight
    
    # Add volume cost: price_per_cubic_cm × volume
    total += pricing_rules['price_per_cubic_cm'] * volume
    
    # Apply express multiplier if needed
    if is_express:
        total *= pricing_rules['express_multiplier']
    
    # Apply destination multiplier
    if destination == 'international':
        total *= pricing_rules['international_multiplier']
    
    # Round to 2 decimal places for currency
    return round(total, 2)

def generate_shipping_alerts(params, alert_rules):
    """
    Generate shipping alerts based on package parameters and alert rules.
    
    Args:
        params (dict): Package parameters:
            - length_cm (float): Length in cm
            - width_cm (float): Width in cm  
            - height_cm (float): Height in cm
            - weight_kg (float): Weight in kg
            - destination (str): 'national' or 'international'
        alert_rules (dict): Alert thresholds from rules.json
        
    Returns:
        list: Alert messages (empty list if no alerts)
    """
    alerts = []
    
    # Extract parameters
    length = float(params.get('length_cm', 0))
    width = float(params.get('width_cm', 0))
    height = float(params.get('height_cm', 0))
    weight = float(params.get('weight_kg', 0))
    destination = params.get('destination', 'national')
    
    # Check for heavy package
    if weight > alert_rules['heavy_weight_kg']:
        alerts.append(f"Heavy package ({weight}kg): special handling may be required")
    
    # Check for oversized dimensions
    max_dimension = max(length, width, height)
    if max_dimension > alert_rules['oversized_cm']:
        alerts.append(f"Oversized dimension ({max_dimension}cm): check transport limits")
    
    # Check for bulky volume
    volume = calculate_volume_cm3(length, width, height)
    if volume > alert_rules['bulky_volume_cm3']:
        alerts.append(f"Bulky package ({volume:.0f}cm³): may require extra space")
    
    # Check for international shipment
    if destination == 'international':
        alerts.append("International shipment: customs documentation may be required")
    
    return alerts