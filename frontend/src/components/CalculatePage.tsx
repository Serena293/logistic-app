// src/components/CalculatePage.tsx
import React, { useState, FormEvent, ChangeEvent } from "react";
import {
  Container,
  Form,
  Button,
  Card,
  Alert,
  Spinner,
  Row,
  Col,
} from "react-bootstrap";
import {
  BoxSeam,
  Rulers,
  GlobeEuropeAfrica,
  Truck,
  ExclamationTriangle,
  InfoCircle,
  Hash,
} from "react-bootstrap-icons";

// TypeScript interfaces
interface ShippingFormData {
  length_cm: string;
  width_cm: string;
  height_cm: string;
  weight_kg: string;
  is_express: boolean;
  destination: "national" | "international";
}

interface PackageSummary {
  dimensions?: {
    length_cm?: number;
    width_cm?: number;
    height_cm?: number;
  };
  weight_kg?: number;
}

interface ApiResponse {
  success: boolean;
  calculation_id?: string;
  total_price?: number;
  currency?: "EUR" | "USD" | string;
  price_breakdown?: Record<string, number>;
  alerts: string[];
  estimated_delivery?: string;
  timestamp?: string;
  package_summary?: PackageSummary;
  error?: string;
}

const CalculatePage: React.FC = () => {
  const [formData, setFormData] = useState<ShippingFormData>({
    length_cm: "",
    width_cm: "",
    height_cm: "",
    weight_kg: "",
    is_express: false,
    destination: "national",
  });

  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    const numericFields: (keyof ShippingFormData)[] = [
      "length_cm",
      "width_cm",
      "height_cm",
      "weight_kg",
    ];

    for (const field of numericFields) {
      const value = parseFloat(formData[field] as string);
      if (isNaN(value) || value <= 0) {
        setError(
          `Please enter a valid positive number for ${field.replace("_", " ")}`,
        );
        setLoading(false);
        return;
      }
    }

    const requestData = {
      length_cm: parseFloat(formData.length_cm),
      width_cm: parseFloat(formData.width_cm),
      height_cm: parseFloat(formData.height_cm),
      weight_kg: parseFloat(formData.weight_kg),
      is_express: formData.is_express,
      destination: formData.destination,
    };

    try {
      const response = await fetch("https://logistic-app-m5tv.onrender.com/api/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData),
      });

      const data: ApiResponse = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "API request failed");
      }

      setResult(data);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "An error occurred while calculating shipping";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      length_cm: "",
      width_cm: "",
      height_cm: "",
      weight_kg: "",
      is_express: false,
      destination: "national",
    });
    setResult(null);
    setError("");
  };

  return (
    <Container className="py-5">
      <h1 className="text-center mb-3">
        <BoxSeam className="me-2 text-primary" />
        Shipping Cost Calculator
      </h1>
      <p className="text-center text-muted mb-5">
        Calculate shipping costs instantly with our automated pricing engine
      </p>

      <Row className="justify-content-center">
        <Col md={8} lg={6}>
          {error && (
            <Alert variant="danger" dismissible onClose={() => setError("")}>
              <ExclamationTriangle className="me-2" />
              {error}
            </Alert>
          )}

          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>
                <Rulers className="me-2" />
                Enter Package Details
              </Card.Title>

              <Form onSubmit={handleSubmit}>
                {/* Dimensions */}
                <Form.Group className="mb-3">
                  <Form.Label>Dimensions (cm)</Form.Label>
                  <Row>
                    {(
                      [
                        "length_cm",
                        "width_cm",
                        "height_cm",
                      ] as (keyof ShippingFormData)[]
                    ).map((field) => (
                      <Col key={field}>
                        <Form.Control
                          type="number"
                          name={field}
                          placeholder={field.replace("_cm", "").toUpperCase()}
                          onChange={handleInputChange}
                          min="0.1"
                          step="0.1"
                          required
                        />
                      </Col>
                    ))}
                  </Row>
                  <Form.Text className="text-muted">
                    Enter dimensions in centimeters
                  </Form.Text>
                </Form.Group>

                {/* Weight */}
                <Form.Group className="mb-3">
                  <Form.Label>Weight (kg)</Form.Label>
                  <Form.Control
                    type="number"
                    name="weight_kg"
                    placeholder="Enter weight in kilograms"
                    value={formData.weight_kg}
                    onChange={handleInputChange}
                    min="0.1"
                    step="0.1"
                    required
                  />
                </Form.Group>

                {/* Destination */}
                <Form.Group className="mb-3">
                  <Form.Label>Destination</Form.Label>
                  <div>
                    <Form.Check
                      inline
                      type="radio"
                      label={
                        <>
                          <Truck className="me-1" /> National
                        </>
                      }
                      name="destination"
                      value="national"
                      checked={formData.destination === "national"}
                      onChange={handleInputChange}
                      id="destination-national"
                    />
                    <Form.Check
                      inline
                      type="radio"
                      label={
                        <>
                          <GlobeEuropeAfrica className="me-1" /> International
                        </>
                      }
                      name="destination"
                      value="international"
                      checked={formData.destination === "international"}
                      onChange={handleInputChange}
                      id="destination-international"
                    />
                  </div>
                </Form.Group>

                {/* Express */}
                <Form.Group className="mb-4">
                  <Form.Check
                    type="switch"
                    name="is_express"
                    label="Express Shipping (faster delivery)"
                    checked={formData.is_express}
                    onChange={handleInputChange}
                    id="express-shipping"
                  />
                  <Form.Text className="text-muted">
                    Express shipping typically arrives 50% faster
                  </Form.Text>
                </Form.Group>

                {/* Buttons */}
                <div className="d-flex gap-2">
                  <Button
                    variant="primary"
                    type="submit"
                    disabled={loading}
                    className="flex-grow-1"
                  >
                    {loading ? (
                      <>
                        <Spinner
                          animation="border"
                          size="sm"
                          className="me-2"
                        />
                        Calculating...
                      </>
                    ) : (
                      "Calculate Shipping Cost"
                    )}
                  </Button>
                  <Button variant="outline-secondary" onClick={handleReset}>
                    Reset
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>

          {result && result.success && (
            <Card className="shadow-sm border-success">
              <Card.Body>
                <Card.Title className="text-success">
                  <InfoCircle className="me-2" />
                  Shipping Calculation Results
                </Card.Title>

                <div className="text-center mb-4">
                  <h2 className="display-5">
                    {result.total_price?.toFixed(2)} {result.currency}
                  </h2>
                  <p className="text-muted">
                    Estimated delivery: {result.estimated_delivery}
                  </p>
                </div>

                {result.package_summary && (
                  <div className="mb-4">
                    <h5>Package Summary</h5>
                    <Row className="text-center">
                      {["length_cm", "width_cm", "height_cm"].map((dim) => (
                        <Col key={dim}>
                          <div className="p-2 border rounded">
                            <div className="fw-bold">
                              {result.package_summary?.dimensions?.[
                                dim as keyof PackageSummary["dimensions"]
                              ] ?? "-"}{" "}
                              cm
                            </div>
                            <small className="text-muted">
                              {dim.replace("_cm", "").toUpperCase()}
                            </small>
                          </div>
                        </Col>
                      ))}
                      <Col>
                        <div className="p-2 border rounded">
                          <div className="fw-bold">
                            {result.package_summary.weight_kg ?? "-"} kg
                          </div>
                          <small className="text-muted">Weight</small>
                        </div>
                      </Col>
                    </Row>
                  </div>
                )}

                {result.alerts.length > 0 && (
                  <div className="mt-4">
                    <h5>
                      <ExclamationTriangle className="me-2 text-warning" />
                      Shipping Alerts
                    </h5>
                    {result.alerts.length > 0 && (
                      <div className="mt-4">
                        <h5>
                          <ExclamationTriangle className="me-2 text-warning" />
                          Shipping Alerts
                        </h5>

                        {result.alerts.map((alert, index) => {
                          let Icon = InfoCircle;
                          let variant: "warning" | "info" = "info";

                          if (alert.toLowerCase().includes("heavy")) {
                            Icon = ExclamationTriangle;
                            variant = "warning";
                          } else if (alert.toLowerCase().includes("package")) {
                            Icon = BoxSeam;
                          } else if (
                            alert.toLowerCase().includes("international")
                          ) {
                            Icon = GlobeEuropeAfrica;
                          }

                          return (
                            <Alert
                              key={index}
                              variant={variant}
                              className="d-flex align-items-center"
                            >
                              <Icon className="me-2" />
                              {alert}
                            </Alert>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}

                {result.calculation_id && (
                  <div className="mt-3 text-end">
                    <small className="text-muted">
                      <Hash className="me-1" />
                      {result.calculation_id}
                    </small>
                  </div>
                )}
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default CalculatePage;
