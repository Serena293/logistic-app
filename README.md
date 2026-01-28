# 🚚 Logistics Shipping Calculator

A full-stack web application for calculating shipping costs with automated alerts and delivery estimates.

## 🌐 Live Demo
- **Frontend:** [https://logistics-app-xyz.web.app](https://logistic-app-fe.onrender.com)
- **Backend API:** [https://logistics-backend-xyz.a.run.app/api/health](https://logistic-app-m5tv.onrender.com)
- **Source Code:** [https://github.com/Serena293/logistic-app](https://github.com/Serena293/logistic-app)

## 🎯 Features

### 📦 Package Analysis
- **Real-time cost calculation** based on dimensions, weight, and destination
- **Volume calculation** in cubic centimeters
- **Automated pricing** with configurable business rules

### ⚠️ Smart Alerts System
- **Heavy package detection** (>20kg threshold)
- **Oversized dimension warnings**
- **International shipment** customs documentation alerts
- **Bulky volume** notifications

### 🌍 Shipping Options
- **National & International** destinations
- **Express shipping** with faster delivery times
- **Delivery time estimates** based on destination and speed

## 🛠️ Tech Stack

### **Backend** (Python)
- **Framework:** Flask
- **API:** RESTful JSON API
- **Containerization:** Docker
- **Deployment:** Google Cloud Run
- **Testing:** pytest with 85%+ coverage

### **Frontend** (TypeScript)
- **Framework:** React 18
- **UI Library:** React Bootstrap with Bootstrap Icons
- **State Management:** React Hooks
- **Routing:** React Router DOM
- **Deployment:** Firebase Hosting

### **DevOps & Tools**
- **Version Control:** Git & GitHub
- **CI/CD:** Manual deployment with automated builds
- **Package Management:** pip & npm
- **Code Quality:** TypeScript strict mode, ESLint


## 🔧 API Documentation

### `POST /api/calculate`
Calculate shipping price and generate alerts.

**Request:**
```json
{
  "length_cm": 30.0,
  "width_cm": 20.0,
  "height_cm": 15.0,
  "weight_kg": 25.0,
  "is_express": true,
  "destination": "international"
}

{
  "success": true,
  "total_price": 85.50,
  "currency": "EUR",
  "alerts": [
    "Heavy package (25kg): special handling may be required",
    "International shipment: customs documentation may be required"
  ],
  "estimated_delivery": "3-5 business days"
}

