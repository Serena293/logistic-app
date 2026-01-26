from flask import Flask
from flask_cors import CORS
import json
import os
from flask import request, jsonify
from datetime import datetime
import hashlib


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


def get_delivery_time(destination, is_express, delivery_times):
    """
    Determine estimated delivery time based on destination and shipping speed.
    
    Args:
        destination (str): 'national' or 'international'
        is_express (bool): True for express shipping, False for standard
        delivery_times (dict): Delivery time configurations from rules.json
        
    Returns:
        str: Estimated delivery time description
        
    Raises:
        KeyError: If delivery time configuration is missing
        
    Example:
        >>> delivery_times = {'national_standard': '3-5 days'}
        >>> get_delivery_time('national', False, delivery_times)
        '3-5 days'
    """
    # Validate inputs
    if destination not in ['national', 'international']:
        raise ValueError("Destination must be 'national' or 'international'")
    
    if not isinstance(is_express, bool):
        raise TypeError("is_express must be a boolean")
    
    # Determine which delivery time key to use
    if destination == 'national':
        time_key = 'national_express' if is_express else 'national_standard'
    else:  # international
        time_key = 'international_express' if is_express else 'international_standard'
    
    # Get delivery time from configuration
    if time_key not in delivery_times:
        available_keys = ', '.join(delivery_times.keys())
        raise KeyError(
            f"Delivery time '{time_key}' not found in rules. "
            f"Available options: {available_keys}"
        )
    
    return delivery_times[time_key]

@app.route('/api/calculate', methods=['POST'])
def calculate_shipping():
    """
    Calculate shipping price and generate alerts for a package.
    
    Expected JSON input:
    {
        "length_cm": 30.0,
        "width_cm": 20.0,
        "height_cm": 15.0,
        "weight_kg": 5.0,
        "is_express": false,
        "destination": "national"
    }
    
    Returns JSON response:
    {
        "success": true,
        "calculation_id": "calc_abc123",
        "total_price": 34.0,
        "currency": "EUR",
        "price_breakdown": {...},
        "alerts": [...],
        "estimated_delivery": "3-5 business days",
        "timestamp": "2024-01-22T10:30:00Z"
    }
    """
    try:
        # Get and validate input
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        # Required fields check
        required_fields = ['length_cm', 'width_cm', 'height_cm', 'weight_kg', 'destination']
        missing_fields = [field for field in required_fields if field not in request_data]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Extract data from global 'data' variable (from rules.json)
        pricing_rules = data.get('pricing', {})
        alert_rules = data.get('alerts', {})
        delivery_times = data.get('delivery_times', {})
        currency = data.get('currency', 'EUR')
        
        # Calculate shipping price
        total_price = calculate_shipping_price(request_data, pricing_rules)
        
        # Generate alerts
        alerts = generate_shipping_alerts(request_data, alert_rules)
        
        # Determine delivery time
        destination = request_data.get('destination', 'national')
        is_express = request_data.get('is_express', False)
        estimated_delivery = get_delivery_time(destination, is_express, delivery_times)
        
        # Create price breakdown for transparency
        price_breakdown = {
            "base_price": pricing_rules.get('base_price', 0),
            "weight_cost": pricing_rules.get('price_per_kg', 0) * request_data.get('weight_kg', 0),
            "volume_cost": pricing_rules.get('price_per_cubic_cm', 0) * 
                          calculate_volume_cm3(
                              request_data.get('length_cm', 0),
                              request_data.get('width_cm', 0),
                              request_data.get('height_cm', 0)
                          ),
            "express_multiplier": pricing_rules.get('express_multiplier', 1.0) 
                                  if is_express else 1.0,
            "destination_multiplier": pricing_rules.get('international_multiplier', 1.0) 
                                      if destination == 'international' else 1.0
        }
        
       
        
        # Generate unique calculation ID
        calculation_data = str(request_data) + str(datetime.utcnow())
        calculation_id = "calc_" + hashlib.md5(calculation_data.encode()).hexdigest()[:8]
        
        response = {
            "success": True,
            "calculation_id": calculation_id,
            "total_price": total_price,
            "currency": currency,
            "price_breakdown": price_breakdown,
            "alerts": alerts,
            "estimated_delivery": estimated_delivery,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "package_summary": {
                "dimensions": {
                    "length_cm": request_data.get('length_cm'),
                    "width_cm": request_data.get('width_cm'),
                    "height_cm": request_data.get('height_cm'),
                    "volume_cm3": calculate_volume_cm3(
                        request_data.get('length_cm', 0),
                        request_data.get('width_cm', 0),
                        request_data.get('height_cm', 0)
                    )
                },
                "weight_kg": request_data.get('weight_kg'),
                "destination": destination,
                "express_shipping": is_express
            }
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        # Handle validation errors
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except KeyError as e:
        # Handle missing configuration errors
        return jsonify({
            "success": False,
            "error": f"Configuration error: {str(e)}"
        }), 500
        
    except Exception as e:
        # Handle any other unexpected errors
        import traceback
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e)
            # In production, don't include traceback
        }), 500
    

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        JSON response with API status and version information
    """
    health_status = {
        "status": "healthy",
        "service": "Shipping Calculator API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoints": {
            "calculate": {
                "method": "POST",
                "path": "/api/calculate",
                "description": "Calculate shipping price and alerts"
            },
            "health": {
                "method": "GET", 
                "path": "/api/health",
                "description": "Health check endpoint"
            }
        },
        "configuration_loaded": bool(data),  # Check if rules.json was loaded
        "rules_loaded": {
            "pricing": "pricing" in data,
            "alerts": "alerts" in data,
            "delivery_times": "delivery_times" in data
        }
    }
    return jsonify(health_status), 200


@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint with API information.
    """
    return jsonify({
        "message": "Shipping Calculator API",
        "documentation": "Use POST /api/calculate to calculate shipping prices",
        "health_check": "GET /api/health",
        "status": "operational"
    }), 200


if __name__ == '__main__':
    """
    Start the Flask development server.
    """
    print("=" * 50)
    print("Shipping Calculator API")
    print("=" * 50)
    print(f"Starting server at: http://localhost:5000")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n Available endpoints:")
    print("  GET  /              - API information")
    print("  GET  /api/health    - Health check")
    print("  POST /api/calculate - Calculate shipping")
    print("\n Configuration loaded:")
    print(f"  Pricing rules: {'✓' if 'pricing' in data else '✗'}")
    print(f"  Alert rules:   {'✓' if 'alerts' in data else '✗'}")
    print(f"  Currency:      {data.get('currency', 'Not set')}")
    print("=" * 50)
    
    # Start the server
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=5000,
        debug=True,      # Auto-reload on code changes
        threaded=True    # Handle multiple requests
    )