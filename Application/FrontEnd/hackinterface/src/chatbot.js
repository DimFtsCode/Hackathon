import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown'; // import react-markdown for better looking responses
import {
  Container, Row, Col, Card, Button, InputGroup, FormControl,
} from 'react-bootstrap';
import './chatbot.css';

const Dashboard = () => {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "Welcome to the Wildfire Safety Assistant! I'm here to provide you with information on wildfire preparedness, prevention strategies, and current weather conditions. Feel free to ask any questions or share your concerns about staying safe during wildfire seasons.",
    },
  ]);
  const [inputText, setInputText] = useState('');

  // State variables to manage suggested questions
  const [showSuggestedQuestions, setShowSuggestedQuestions] = useState(true);
  const [hasUserSentMessage, setHasUserSentMessage] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (inputText.trim() === '') return;

    // Hide the suggested questions after the first message is sent
    setHasUserSentMessage(true);
    setShowSuggestedQuestions(false);

    // Add the user's message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: 'user', text: inputText },
      { sender: 'bot', text: 'Typing...', loading: true },
    ]);
    const userMessage = inputText;
    setInputText('');

    try {
      // Send the user's message to the backend
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      // Replace the 'Typing...' message with the actual reply
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.loading ? { sender: 'bot', text: data.reply } : msg
        )
      );
    } catch (error) {
      console.error('Error fetching bot response:', error);
      // Replace the 'Typing...' message with an error message
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.loading
            ? { sender: 'bot', text: 'Sorry, something went wrong.' }
            : msg
        )
      );
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  // Function to handle when a suggested question is clicked
  const handleSuggestedQuestion = (question) => {
    setInputText(question);
    handleSend();
  };

  // Array of suggested questions
  const suggestedQuestions = [
    'What is the wildfire risk today?',
    'How can I prepare my home for a wildfire?',
    'Are there any active wildfires nearby?',
    'What are the weather conditions today?',
    'How do I create an evacuation plan?',
  ];

  return (
    <Container fluid className="p-3">
      <Row className="justify-content-center">
        <Col md={6}>
          <Card>
            <Card.Header as="h5">
              Wildfire Safety Assistant
            </Card.Header>

            {/* Suggested Questions Section */}
            {!hasUserSentMessage ? (
              // Before the user sends a message, show the suggested questions
              <div style={{ padding: '10px', textAlign: 'center' }}>
                <p>Here are some common questions:</p>
                <div className="suggested-questions" style={{ maxHeight: showSuggestedQuestions ? '500px' : '0' }}>
                  {suggestedQuestions.map((question, idx) => (
                    <Button
                      key={idx}
                      variant="outline-secondary"
                      size="sm"
                      style={{ margin: '5px' }}
                      onClick={() => handleSuggestedQuestion(question)}
                    >
                      {question}
                    </Button>
                  ))}
                </div>
              </div>
            ) : (
              // After the user sends a message, show the toggleable text and suggested questions
              <div style={{ padding: '10px', textAlign: 'center' }}>
              <p
                onClick={() => setShowSuggestedQuestions(!showSuggestedQuestions)}
                style={{ cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}
              >
                {showSuggestedQuestions ? 'Hide common questions ▲' : 'Show common questions ▼'}
              </p>
                {showSuggestedQuestions && (
                  <div>
                    {suggestedQuestions.map((question, idx) => (
                      <Button
                        key={idx}
                        variant="outline-secondary"
                        size="sm"
                        style={{ margin: '5px' }}
                        onClick={() => handleSuggestedQuestion(question)}
                      >
                        {question}
                      </Button>
                    ))}
                  </div>
                )}
              </div>
            )}

            <Card.Body style={{ height: '500px', overflowY: 'auto' }}>
              {messages.map((message, idx) => (
                <div
                  key={idx}
                  className={`d-flex mb-3 ${
                    message.sender === 'user'
                      ? 'justify-content-end'
                      : 'justify-content-start'
                  }`}
                >
                  <div style={{ maxWidth: '75%' }}>
                    <div
                      className={`p-2 rounded ${
                        message.sender === 'user'
                          ? 'bg-primary text-white'
                          : 'bg-light'
                      }`}
                    >
                      {message.sender === 'bot' ? (
                        <ReactMarkdown>{message.text}</ReactMarkdown>
                      ) : (
                        <span>{message.text}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </Card.Body>
            <Card.Footer>
              <InputGroup>
                <FormControl
                  placeholder="Type your message..."
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyUp={handleKeyPress}
                  style={{ height: '100%' }} // Διασφαλίζει ότι το FormControl έχει το σωστό ύψος
                />
                <Button
                  variant="primary"
                  onClick={handleSend}
                  style={{ height: '100%' }} // Διασφαλίζει ότι το Button έχει το ίδιο ύψος
                >
                  Send
                </Button>
              </InputGroup>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;