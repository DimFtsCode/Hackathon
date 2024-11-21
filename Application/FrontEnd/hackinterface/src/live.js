import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Tabs, Tab, Card, Spinner, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./live.css";

const Live = () => {
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [openReports, setOpenReports] = useState({});
    const [reloadKey, setReloadKey] = useState(Date.now()); // Initialize with a timestamp to trigger the first load

    const northRegions = [
        "Anthousa", "Melissia", "Vrilissia", "Kifisia",
        "Nea Erythraia", "Ekali", "Rapentosa", "Rodopoli",
        "Vothon", "Grammatiko", "Kato Soulion", "Marathonas",
        "Ntaou Penteli", "Dioni", "Kallitechnoupoli", "Ntrafi"
    ];

    const eastRegions = [
        "Parnis", "Acharnes", "Ano Liosia", "Fyli", "Aspropyrgos",
        "Skourta", "Moni Osiou Meletiou", "Avlonas", "Varympompi",
        "Afidnes", "Agia Triada", "Malakasa", "Aigeirouses"
    ];

    const fetchPredictions = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/latest-predictions");
            setPredictions(response.data.data);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching predictions:", error);
            setLoading(false);
        }
    };

    const reloadIframe = () => {
        setReloadKey(Date.now()); // Update reloadKey to force iframe reload
    };

    const toggleReport = (id) => {
        setOpenReports((prev) => ({
            ...prev,
            [id]: !prev[id],
        }));
    };

    const getButtonVariant = (predictionValue) => {
        if (predictionValue <= 0.4) return "primary"; // Blue
        if (predictionValue <= 0.8) return "warning"; // Yellow
        return "danger"; // Red
    };

    const getButtonLabel = (isOpen) => (isOpen ? "Hide Report" : "Show Report");

    useEffect(() => {
        fetchPredictions();
        const intervalId = setInterval(() => {
            fetchPredictions();
            reloadIframe(); // Refresh the iframe every minute
        }, 60000);

        return () => clearInterval(intervalId);
    }, []);

    const filteredPredictions = (regions) => {
        return predictions.filter(prediction => regions.includes(prediction.name));
    };

    const renderFormattedMessage = (message) => {
        const lines = message.split("\n").filter(line => line.trim() !== "");
        return (
            <ul>
                {lines.map((line, index) => (
                    <li key={index} style={{ marginBottom: "10px" }}>
                        {line}
                    </li>
                ))}
            </ul>
        );
    };

    return (
        <Container 
            className="mt-5 border rounded p-3"
            style={{
                backgroundColor: "rgba(128, 128, 128, 1)",
                border: "1px solid rgba(0, 0, 0, 0.1)", 
                backdropFilter: "blur(10px)"
            }}
        >
            {loading ? (
                <div className="text-center">
                    <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>
                </div>
            ) : (
                <Tabs defaultActiveKey="north" id="region-tabs" className="mb-3">
                    {/* Tab for North Regions */}
                    <Tab eventKey="north" title="North Regions">
                        {filteredPredictions(northRegions).map((prediction) => (
                            <Card className="mb-4" key={prediction._id}>
                                <Card.Body>
                                    <Card.Title className="mb-3">{prediction.name}</Card.Title>
                                    <Card.Subtitle className="mb-3 text-muted">
                                        {prediction.date} {prediction.time}
                                    </Card.Subtitle>
                                    <div className="d-flex flex-nowrap justify-content-between">
                                        <div><strong>Temperature:</strong> {prediction.temperature}°C</div>
                                        <div><strong>Wind Speed:</strong> {prediction.wind_speed} km/h</div>
                                        <div><strong>Wind Direction:</strong> {prediction.wind_dir}°</div>
                                        <div><strong>Humidity:</strong> {prediction.humidity}%</div>
                                        <div><strong>Visibility:</strong> {prediction.visibility} km</div>
                                    </div>
                                    <div className="mt-3">
                                        <Button 
                                            variant={getButtonVariant(prediction.prediction)}
                                            onClick={() => toggleReport(prediction._id)}
                                            style={{ textDecoration: "none" }}
                                        >
                                            {getButtonLabel(openReports[prediction._id])}
                                        </Button>
                                        {openReports[prediction._id] && (
                                            <div className="mt-2">
                                                <strong>Report:</strong>
                                                {renderFormattedMessage(prediction.message)}
                                            </div>
                                        )}
                                    </div>
                                </Card.Body>
                            </Card>
                        ))}
                    </Tab>

                    {/* Tab for East Regions */}
                    <Tab eventKey="east" title="East Regions">
                        {filteredPredictions(eastRegions).map((prediction) => (
                            <Card className="mb-4" key={prediction._id}>
                                <Card.Body>
                                    <Card.Title className="mb-3">{prediction.name}</Card.Title>
                                    <Card.Subtitle className="mb-3 text-muted">
                                        {prediction.date} {prediction.time}
                                    </Card.Subtitle>
                                    <div className="d-flex flex-nowrap justify-content-between">
                                        <div><strong>Temperature:</strong> {prediction.temperature}°C</div>
                                        <div><strong>Wind Speed:</strong> {prediction.wind_speed} km/h</div>
                                        <div><strong>Wind Direction:</strong> {prediction.wind_dir}°</div>
                                        <div><strong>Humidity:</strong> {prediction.humidity}%</div>
                                        <div><strong>Visibility:</strong> {prediction.visibility} km</div>
                                    </div>
                                    <div className="mt-3">
                                        <Button 
                                            variant={getButtonVariant(prediction.prediction)}
                                            onClick={() => toggleReport(prediction._id)}
                                            style={{ textDecoration: "none" }}
                                        >
                                            {getButtonLabel(openReports[prediction._id])}
                                        </Button>
                                        {openReports[prediction._id] && (
                                            <div className="mt-2">
                                                <strong>Report:</strong>
                                                {renderFormattedMessage(prediction.message)}
                                            </div>
                                        )}
                                    </div>
                                </Card.Body>
                            </Card>
                        ))}
                    </Tab>

                    {/* Tab for Map */}
                    <Tab eventKey="map" title="Map">
                        <div style={{ width: '100%', height: '100vh' }}>
                            <iframe
                                key={reloadKey}
                                src="map_colored.html"
                                title="Athens Map"
                                width="100%"
                                height="100%"
                                style={{ border: 'none' }}
                            />
                        </div>
                    </Tab>
                </Tabs>
            )}
        </Container>
    );
};

export default Live;
