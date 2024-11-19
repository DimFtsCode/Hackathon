import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Tabs, Tab, Card, Spinner } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./live.css";

const Live = () => {
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);

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

    useEffect(() => {
        const socket = new WebSocket("ws://127.0.0.1:8000/ws");

        socket.onopen = () => {
            console.log("WebSocket connection established.");
            fetchPredictions();
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log("Message received from WebSocket:", data);
                if (data.message === "New data available") {
                    fetchPredictions();
                }
            } catch (error) {
                console.error("Error parsing WebSocket message:", error);
            }
        };

        socket.onclose = (event) => {
            console.warn("WebSocket connection closed:", event);
            fetchPredictions();
        };

        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
            fetchPredictions();
        };

        const intervalId = setInterval(() => {
            if (socket.readyState === WebSocket.CLOSED) {
                console.warn("WebSocket is closed. Fetching predictions...");
                fetchPredictions();
            }
        }, 300000);

        return () => {
            console.log("Cleaning up WebSocket connection.");
            clearInterval(intervalId);
            socket.close();
        };
    }, []);

    const filteredPredictions = (regions) => {
        return predictions.filter(prediction => regions.includes(prediction.name));
    };

    const renderFormattedMessage = (message) => {
        const lines = message.split("\n").filter(line => line.trim() !== ""); // Χωρισμός γραμμών
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
                backgroundColor: "rgba(128, 128, 128, 1)", // Grey with full opacity
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
                                        <div><strong>Latitude:</strong> {prediction.latitude}</div>
                                        <div><strong>Longitude:</strong> {prediction.longitude}</div>
                                        <div><strong>Temperature:</strong> {prediction.temperature}°C</div>
                                        <div><strong>Wind Speed:</strong> {prediction.wind_speed} km/h</div>
                                        <div><strong>Wind Direction:</strong> {prediction.wind_dir}°</div>
                                        <div><strong>Humidity:</strong> {prediction.humidity}%</div>
                                        <div><strong>Visibility:</strong> {prediction.visibility} km</div>
                                    </div>
                                    <div className="mt-3">
                                        <strong>Report:</strong>
                                        {renderFormattedMessage(prediction.message)}
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
                                        <div><strong>Latitude:</strong> {prediction.latitude}</div>
                                        <div><strong>Longitude:</strong> {prediction.longitude}</div>
                                        <div><strong>Temperature:</strong> {prediction.temperature}°C</div>
                                        <div><strong>Wind Speed:</strong> {prediction.wind_speed} km/h</div>
                                        <div><strong>Wind Direction:</strong> {prediction.wind_dir}°</div>
                                        <div><strong>Humidity:</strong> {prediction.humidity}%</div>
                                        <div><strong>Visibility:</strong> {prediction.visibility} km</div>
                                    </div>
                                    <div className="mt-3">
                                        <strong>Report:</strong>
                                        {renderFormattedMessage(prediction.message)}
                                    </div>
                                </Card.Body>
                            </Card>
                        ))}
                    </Tab>
                </Tabs>
            )}
        </Container>
    );
};

export default Live;
