import React, { useRef } from "react";

const Help = () => {
  const chatbotRef = useRef(null);
  const demoRef = useRef(null);
  const liveRef = useRef(null);

  const scrollToSection = (ref) => {
    ref.current.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div
      style={{
        margin: "50px auto",
        maxWidth: "800px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center" }}>Help</h1>
      <p>
        Welcome to the Fire Monitor system! Here you can find information and
        guidance on how to use the application effectively. There are three
        features:
        <ul>
          <li>
            <button
              style={{
                background: "none",
                color: "darkblue",
                border: "none",
                cursor: "pointer",
                textDecoration: "underline",
                fontSize: "inherit",
                padding: 0,
              }}
              onClick={() => scrollToSection(chatbotRef)}
            >
              Chatbot
            </button>
          </li>
          <li>
            <button
              style={{
                background: "none",
                color: "darkblue",
                border: "none",
                cursor: "pointer",
                textDecoration: "underline",
                fontSize: "inherit",
                padding: 0,
              }}
              onClick={() => scrollToSection(demoRef)}
            >
              Fire Monitor Demo
            </button>
          </li>
          <li>
            <button
              style={{
                background: "none",
                color: "darkblue",
                border: "none",
                cursor: "pointer",
                textDecoration: "underline",
                fontSize: "inherit",
                padding: 0,
              }}
              onClick={() => scrollToSection(liveRef)}
            >
              Fire Monitor Live
            </button>
          </li>
        </ul>
      </p>

      {/* Chatbot Section */}
      <div
        ref={chatbotRef}
        style={{
          border: "3px solid grey",
          padding: "15px",
          borderRadius: "5px",
          marginTop: "20px",
          backgroundColor: "#f8f9fa",
        }}
      >
        <h2>Chatbot</h2>
        <p>
          The chatbot feature allows you to ask questions about the fire
          monitoring system. Here you can get guidance on fire safety
          measures,ask about past fire in the areas but also about current fire
          risks in specific regions. Simply type your query into the chatbot
          window, and it will provide an instant response.
        </p>
      </div>

      {/* Fire Monitor Demo Section */}
      <div
        ref={demoRef}
        style={{
          border: "3px solid grey",
          padding: "15px",
          borderRadius: "5px",
          marginTop: "20px",
          backgroundColor: "#f8f9fa",
        }}
      >
        <h2>Fire Monitor Demo</h2>
        <p>
          The Fire Monitor Demo operates during the fire season, starting from{" "}
          <strong>June 5th, 2024</strong>, and running until{" "}
          <strong>October 31st, 2024</strong>. During this period, the system
          collects and processes forecast data every three hours to generate
          detailed reports.
        </p>
        <p>
          These reports provide valuable insights into weather patterns and fire
          risk predictions. The demo environment allows users to understand how
          the system works, view sample data, and explore its features without
          affecting live operations.
        </p>
      </div>

      {/* Fire Monitor Live Section */}
      <div
        ref={liveRef}
        style={{
          border: "3px solid grey",
          padding: "15px",
          borderRadius: "5px",
          marginTop: "20px",
          backgroundColor: "#f8f9fa",
        }}
      >
        <h2>Fire Monitor Live</h2>
        <p>
          The "Fire Monitor Live" feature provides real-time monitoring and
          predictions for fire risks in the East and North regions of Attiki. It
          includes the following functionalities:
        </p>
        <ul>
          <li>
            <strong>Live Forecast:</strong> Displays current weather data such
            as temperature, wind speed, humidity, and visibility for each
            monitored area.
          </li>
          <li>
            <strong>Fire Risk Levels:</strong> Predicts the likelihood of fires
            in the monitored regions.
          </li>
          <li>
            <strong>Drone Deployment:</strong>
            <ul>
              <li>
                For medium fire risk, drones are activated from the nearest
                "Drone Take Off Area" to detect potential fires.
              </li>
              <li>
                The system calculates the arrival time and flight direction for
                efficient coverage.
              </li>
            </ul>
          </li>
          <li>
            <strong>High Risk Response:</strong>
            <ul>
              <li>
                Automatically alerts the nearest fire stations and police
                departments to take action.
              </li>
              <li>
                Identifies and prioritizes the protection of critical points
                like schools, hospitals, and theaters in the area.
              </li>
              <li>
                Provides directions and estimated response times to emergency
                services.
              </li>
            </ul>
          </li>
        </ul>

        {/* How to Use the System */}
        <div>
          <h3>How to Use the System</h3>
          <ol>
            <li>Navigate to the "Fire Monitor Live" section.</li>
            <li>
              Select the region (East or North) to view its live data and fire
              risk report.
            </li>
            <li>
              Review the recommended actions and take necessary precautions.
            </li>
          </ol>
        </div>
      </div>
      {/* FAQs */}
      <div
        style={{
          border: "3px solid grey",
          padding: "15px",
          borderRadius: "5px",
          marginTop: "20px",
          backgroundColor: "#f8f9fa",
        }}
      >
        <h2>FAQs</h2>
        <p>
          <strong>Q:</strong> What can I ask the chatbot?
          <br />
          <strong>A:</strong> You can ask the chatbot about current fire risks,
          safety measures, or system functionality. It provides instant answers
          based on your queries.
        </p>
        <p>
          <strong>Q:</strong> What if the chatbot doesn’t respond?
          <br />
          <strong>A:</strong> Check your internet connection and refresh the
          page. If the issue persists, contact support.
        </p>
        <p>
          <strong>Q:</strong> What is the purpose of the demo?
          <br />
          <strong>A:</strong> The demo allows you to explore the system features
          in a controlled environment without affecting real-world data.
        </p>
        <p>
          <strong>Q:</strong> Can I test real data in the demo?
          <br />
          <strong>A:</strong> No, the demo is designed to simulate data for
          learning and exploration purposes only.
        </p>
        <p>
          <strong>Q:</strong> How accurate is the live data?
          <br />
          <strong>A:</strong> The data is updated in real-time using reliable
          weather and geographic sources, ensuring high accuracy.
        </p>
        <p>
          <strong>Q:</strong> What happens when a medium fire risk is detected?
          <br />
          <strong>A:</strong> Drones are automatically deployed from the nearest
          "Drone Take Off Area" to supervise the area and provide additional
          data.
        </p>
        <p>
          <strong>Q:</strong> How are high-risk areas managed?
          <br />
          <strong>A:</strong> The system notifies nearby fire stations and
          police departments, calculates response times, and provides a plan to
          protect critical locations.
        </p>
      </div>
    </div>
  );
};

export default Help;
