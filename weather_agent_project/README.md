Google ADK Multi-Agent Weather Bot
This project is a multi-agent, stateful AI system built using the Google Agent Development Kit (ADK). It is designed to fetch the weather for a given city by orchestrating a robust, multi-step workflow.

This system demonstrates several advanced agentic design patterns:

Multi-Agent Hierarchy: A "Coordinator" agent manages a team of specialized sub-agents.    

A2A Delegation: The Coordinator delegates conversational tasks (like "hello") to a GreetingAgent and all weather-related tasks to a WeatherPipelineAgent.    

Multi-Tool Use: The system uses two distinct tools: tool_get_coordinates (to find a city's lat/lon) and tool_get_weather (to get the weather from those coordinates).    

Workflow Orchestration: A SequentialAgent is used to create a reliable, "software-defined" pipeline, ensuring the geocoding tool always runs before the weather tool.    

Session Management: The agent uses session state for two purposes:

To pass data between agents (piping the coordinates from Step 1 to Step 2).    

To create conversational memory (remembering the last weather report to answer follow-up questions).    

Tech Stack
Python 3.9+

Google Agent Development Kit (ADK)    

Google Gemini API (using gemini-2.5-flash)

Open-Meteo API (for free, no-API-key geocoding and weather data)

Setup and Installation
**Clone the repository:**bash git clone https://github.com/YourUsername/weather-agent-project.git cd weather-agent-project


Create and activate a Python virtual environment:

Bash

python -m venv.venv
source.venv/bin/activate
# On Windows, use:.venv\Scripts\activate.bat
Install dependencies:

Bash

pip install google-adk requests
Set up your API Key: This project requires a Google Gemini API key.    

Create a new file in the root of the project named .env.

Add your API key and the Google ADK configuration to this file:

Code snippet

GOOGLE_API_KEY="YOUR_API_KEY_HERE"
GOOGLE_GENAI_USE_VERTEXAI="False"
(The .gitignore file will prevent this file from ever being uploaded to GitHub).

How to Run
This agent is designed for multi-turn, stateful conversations. The best way to run it is using the adk web command.

From the project's root directory, run the ADK web server:

Bash

adk web --port 8000
Open your web browser and navigate to: http://localhost:8000

Example Test Plan
You can test the agent's different capabilities in the web UI:

Test 1: A2A Delegation (Greeting)

You: Hello there

Agent: (Responds with a simple greeting, without running the weather pipeline).

Test 2: Multi-Agent Pipeline (Weather)

You: What is the weather in New York?

Agent: (Runs the full geocoding_agent -> weather_report_agent pipeline and gives the temperature).

Test 3: Session Management (Memory)

You: What was that temperature again?

Agent: (The CoordinatorAgent answers from its memory without re-running the pipeline).