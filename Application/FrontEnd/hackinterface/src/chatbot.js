import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown'; // import react-markdown for better looking responses
import {
  Container, Row, Col, Card, Form, Button, InputGroup, FormControl,
} from 'react-bootstrap';
import { useRef, useEffect } from 'react';



const Dashboard = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Hello! How can I assist you today?' },
    ]);
    const [inputText, setInputText] = useState('');

    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (inputText.trim() === '') return;
  
    // Add the user's message to the chat
    setMessages([...messages, { sender: 'user', text: inputText }]);
    const userMessage = inputText;
    setInputText('');

    setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Typing...', loading: true },
      ]);
  
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
  
      // Add the bot's response to the chat
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.loading
            ? { sender: 'bot', text: data.reply }
            : msg
        )
      );
    } catch (error) {
      console.error('Error fetching bot response:', error);
      // Optionally, display an error message in the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Sorry, something went wrong.' },
      ]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <Container fluid className="p-3">
      <Row className="justify-content-center">
        <Col md={6}>
          <Card>
            <Card.Header as="h5">Chat with Our Assistant</Card.Header>
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
            </Card.Body>
            <Card.Footer>
              <InputGroup>
                <FormControl
                  placeholder="Type your message..."
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyUp={handleKeyPress}
                />
                <Button variant="primary" onClick={handleSend}>
                  Send
                </Button>
              </InputGroup>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
      <div ref={messagesEndRef} />
    </Container>
  );
};

export default Dashboard;