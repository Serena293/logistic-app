import React from 'react';
import { Container, Button, Card, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import {
  BoxSeam,
  CashStack,
  ExclamationTriangle,
  Rulers,
  GlobeEuropeAfrica,
  LightningCharge
} from 'react-bootstrap-icons';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container className="py-5">
      <Row className="justify-content-center align-items-center">
        <Col lg={8} className="text-center">
          <h1 className="display-4 fw-bold mb-4">
            Smart Logistics Calculator
          </h1>

          <p className="lead mb-5">
            Calculate shipping costs instantly with our AI-powered logistics platform.
            Get accurate pricing, automated alerts, and delivery estimates for your packages.
          </p>

          <Card className="shadow-lg border-0 mb-5">
            <Card.Body className="p-5">
              <div className="mb-4">
                <div className="d-flex justify-content-center mb-4 gap-4">
                  <div className="text-center">
                    <BoxSeam size={40} className="text-primary mb-2" />
                    <div className="fw-bold">Package Analysis</div>
                  </div>

                  <div className="text-center">
                    <CashStack size={40} className="text-success mb-2" />
                    <div className="fw-bold">Instant Pricing</div>
                  </div>

                  <div className="text-center">
                    <ExclamationTriangle size={40} className="text-warning mb-2" />
                    <div className="fw-bold">Smart Alerts</div>
                  </div>
                </div>

                <p className="mb-4">
                  Our platform analyzes your package dimensions, weight, and destination
                  to provide real-time shipping costs and important alerts for your logistics needs.
                </p>
              </div>

              <Button
                variant="primary"
                size="lg"
                onClick={() => navigate('/calculate')}
                className="px-5 py-3"
              >
                Start Calculating →
              </Button>
            </Card.Body>
          </Card>

          <Row className="mt-5">
            <Col md={4} className="mb-4">
              <div className="p-4 border rounded h-100 text-center">
                <Rulers size={32} className="text-primary mb-3" />
                <h5>Accurate Dimensions</h5>
                <p>
                  Calculate costs based on precise package measurements in centimeters.
                </p>
              </div>
            </Col>

            <Col md={4} className="mb-4">
              <div className="p-4 border rounded h-100 text-center">
                <GlobeEuropeAfrica size={32} className="text-success mb-3" />
                <h5>Global Shipping</h5>
                <p>
                  National and international shipping with customs alerts.
                </p>
              </div>
            </Col>

            <Col md={4} className="mb-4">
              <div className="p-4 border rounded h-100 text-center">
                <LightningCharge size={32} className="text-warning mb-3" />
                <h5>Real-time Alerts</h5>
                <p>
                  Get notified about special handling requirements instantly.
                </p>
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default HomePage;
