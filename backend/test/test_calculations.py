# test/test_calculations.py
"""
Unit tests for shipping calculation functions.
Tests for:
- calculate_volume_cm3
- calculate_shipping_price  
- generate_shipping_alerts
"""

import sys
import os
import json

# Add parent directory to path to import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from app.py
from app import calculate_volume_cm3, calculate_shipping_price, generate_shipping_alerts


class TestVolumeCalculations:
    """Test suite for calculate_volume_cm3 function"""
    
    def test_volume_small_package(self):
        """Test volume calculation for a small package"""
        result = calculate_volume_cm3(10, 5, 2)
        expected = 100  # 10 * 5 * 2 = 100
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_volume_large_package(self):
        """Test volume calculation for a large package"""
        result = calculate_volume_cm3(100, 50, 30)
        expected = 150000  # 100 * 50 * 30 = 150000
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_volume_zero_dimension(self):
        """Test volume with zero dimension"""
        result = calculate_volume_cm3(10, 0, 5)
        expected = 0  # 10 * 0 * 5 = 0
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_volume_decimal_values(self):
        """Test volume with decimal dimensions"""
        result = calculate_volume_cm3(10.5, 2.2, 3.0)
        expected = 69.3  # 10.5 * 2.2 * 3.0 = 69.3
        # Use approx for floating point comparison
        assert abs(result - expected) < 0.001, f"Expected ~{expected}, got {result}"


class TestPriceCalculations:
    """Test suite for calculate_shipping_price function"""
    
    def setup_method(self):
        """Setup test pricing rules"""
        self.pricing_rules = {
            'base_price': 5.0,
            'price_per_kg': 2.0,
            'price_per_cubic_cm': 0.001,
            'express_multiplier': 1.5,
            'international_multiplier': 2.0
        }
    
    def test_price_national_standard(self):
        """Test price for national standard shipping"""
        params = {
            'length_cm': 30,
            'width_cm': 20,
            'height_cm': 15,
            'weight_kg': 10,
            'destination': 'national',
            'is_express': False
        }
        result = calculate_shipping_price(params, self.pricing_rules)
        # Calculation:
        # base: 5
        # weight: 10 * 2 = 20
        # volume: 30*20*15=9000 * 0.001 = 9
        # total: 5 + 20 + 9 = 34
        expected = 34.0
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_price_international_express(self):
        """Test price for international express shipping"""
        params = {
            'length_cm': 30,
            'width_cm': 20,
            'height_cm': 15,
            'weight_kg': 5,
            'destination': 'international',
            'is_express': True
        }
        result = calculate_shipping_price(params, self.pricing_rules)
        # Calculation:
        # base: 5
        # weight: 5 * 2 = 10
        # volume: 9000 * 0.001 = 9
        # subtotal: 5 + 10 + 9 = 24
        # express: 24 * 1.5 = 36
        # international: 36 * 2.0 = 72
        expected = 72.0
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_price_validation_negative_values(self):
        """Test that negative values raise ValueError"""
        params = {
            'length_cm': -10,  # Negative!
            'width_cm': 20,
            'height_cm': 15,
            'weight_kg': 5,
            'destination': 'national',
            'is_express': False
        }
        try:
            calculate_shipping_price(params, self.pricing_rules)
            assert False, "Should have raised ValueError for negative length"
        except ValueError as e:
            assert "negative" in str(e).lower()


class TestAlertGeneration:
    """Test suite for generate_shipping_alerts function"""
    
    def setup_method(self):
        """Setup test alert rules"""
        self.alert_rules = {
            'heavy_weight_kg': 20,
            'oversized_cm': 100,
            'bulky_volume_cm3': 50000
        }
    
    def test_no_alerts_normal_package(self):
        """Test no alerts for normal package"""
        params = {
            'weight_kg': 10,
            'length_cm': 30,
            'width_cm': 20,
            'height_cm': 15,
            'destination': 'national'
        }
        alerts = generate_shipping_alerts(params, self.alert_rules)
        assert len(alerts) == 0, f"Expected 0 alerts, got {alerts}"
    
    def test_heavy_package_alert(self):
        """Test alert for heavy package"""
        params = {
            'weight_kg': 25,  # > 20kg threshold
            'length_cm': 30,
            'width_cm': 20,
            'height_cm': 15,
            'destination': 'national'
        }
        alerts = generate_shipping_alerts(params, self.alert_rules)
        assert len(alerts) == 1, f"Expected 1 alert, got {len(alerts)}"
        assert "heavy" in alerts[0].lower()
    
    def test_oversized_alert(self):
        """Test alert for oversized dimension"""
        params = {
            'weight_kg': 5,
            'length_cm': 150,  # > 100cm threshold
            'width_cm': 20,
            'height_cm': 15,
            'destination': 'national'
        }
        alerts = generate_shipping_alerts(params, self.alert_rules)
        assert len(alerts) == 1, f"Expected 1 alert, got {len(alerts)}"
        assert "oversized" in alerts[0].lower()
    
    def test_international_shipment_alert(self):
        """Test info alert for international shipment"""
        params = {
            'weight_kg': 5,
            'length_cm': 30,
            'width_cm': 20,
            'height_cm': 15,
            'destination': 'international'
        }
        alerts = generate_shipping_alerts(params, self.alert_rules)
        assert len(alerts) == 1, f"Expected 1 alert, got {len(alerts)}"
        assert "international" in alerts[0].lower()
    
    def test_multiple_alerts(self):
        """Test multiple alerts triggered together"""
        params = {
            'weight_kg': 25,  # Heavy
            'length_cm': 150,  # Oversized
            'width_cm': 20,
            'height_cm': 15,
            'destination': 'international'  # International
        }
        alerts = generate_shipping_alerts(params, self.alert_rules)
        assert len(alerts) == 3, f"Expected 3 alerts, got {len(alerts)}"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])