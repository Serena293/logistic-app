// src/components/NotFoundPage.tsx
import React from 'react';
import { Container, Button, Card } from 'react-bootstrap';
import { 
  Truck, 
  ExclamationTriangle, 
  ArrowLeft,
  HouseDoor 
} from 'react-bootstrap-icons';
import { useNavigate } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container className="py-5">
      <div className="text-center">
        
        <div className="mb-4">
          <Truck size={80} className="text-muted mb-3" />
          <ExclamationTriangle size={60} className="text-warning" />
        </div>

        <h1 className="display-1 fw-bold text-muted">404</h1>
        
        <h2 className="mb-4">
          <ExclamationTriangle className="text-warning me-2" />
          Page Not Found
        </h2>
        
        <p className="lead mb-5">
          The shipping route you're looking for doesn't exist or has been moved.
        </p>

        <Card className="border-warning shadow-sm mb-5 mx-auto" style={{ maxWidth: '500px' }}>
          <Card.Body className="text-start">
            <h5 className="mb-3">
              <ExclamationTriangle className="text-warning me-2" />
              Possible reasons:
            </h5>
            <ul className="list-unstyled">
              <li className="mb-2">• The page address was typed incorrectly</li>
              <li className="mb-2">• The page has been moved or deleted</li>
              <li className="mb-2">• You followed an outdated link</li>
            </ul>
          </Card.Body>
        </Card>

        <div className="d-flex justify-content-center gap-3">
          <Button 
            variant="primary" 
            onClick={() => navigate('/')}
            className="d-flex align-items-center gap-2"
          >
            <HouseDoor /> Go to Homepage
          </Button>
          
          <Button 
            variant="outline-secondary" 
            onClick={() => navigate(-1)}
            className="d-flex align-items-center gap-2"
          >
            <ArrowLeft /> Go Back
          </Button>
        </div>


        <div className="mt-5 pt-5 border-top">
          <p className="text-muted small">
            While you're here, did you know our shipping calculator can handle 
            packages up to 500kg? Try it out!
          </p>
          <Button 
            variant="outline-primary" 
            size="sm"
            onClick={() => navigate('/calculate')}
          >
            Try Shipping Calculator
          </Button>
        </div>
      </div>
    </Container>
  );
};

export default NotFoundPage;