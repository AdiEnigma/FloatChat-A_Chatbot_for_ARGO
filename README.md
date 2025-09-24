<div align="center">

🌊 FloatChat: Your Conversational Gateway to ARGO Ocean Data

<p>
An AI-powered chatbot that transforms how we discover and visualize complex ARGO oceanographic data, making it accessible to everyone through simple, natural language.
</p>

<p>
<img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/Framework-Streamlit-red.svg" alt="Streamlit">
<img src="https://img.shields.io/badge/NLU-Rasa-orange.svg" alt="Rasa">
<img src="https://img.shields.io/badge/Visualization-Plotly-purple.svg" alt="Plotly">
<img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

</div>

🎥 Demo

A brief GIF showcasing the chatbot in action. Asking a question and receiving an interactive plot.

``
![FloatChat Demo GIF](link_to_your_demo_gif.gif)

## 📖 About The Project

ARGO is a global array of thousands of robotic floats that measure temperature and salinity in the world's oceans, providing a treasure trove of data for climate science. However, accessing this data requires specialized knowledge of programming and complex file formats, creating a high barrier for students, policymakers, and even many researchers.

FloatChat solves this problem by providing an intuitive conversational interface. It replaces the need for code with simple, plain-English questions, allowing anyone to explore this vital dataset and get back instant, interactive visualizations.

## ✨ Key Features

    💬 Conversational Interface: Ask questions in natural language, just like talking to a person.

    🤖 AI-Powered NLU: Utilizes a Natural Language Understanding model to accurately interpret user intent and extract key details.

    📊 On-the-Fly Visualization: Generates rich, interactive Plotly charts and maps in real-time in response to queries.

    💻 Zero-Code Access: No programming knowledge is required to explore the data, democratizing access to scientific insights.

## 🛠️ Technology Stack & Rationale

This project leverages a modern, Python-based stack, chosen for its power and efficiency in building data-centric AI applications.
Component	Technology	Why It Was Chosen
Frontend	Streamlit	For its incredible speed in building beautiful, interactive data apps with pure Python. Perfect for rapid prototyping and hackathons.
Backend & Core Logic	Python	The de facto language for data science and AI, with an unparalleled ecosystem of libraries.
NLU Engine	Rasa	A powerful, open-source framework for building conversational AI, offering full control over the NLU pipeline and dialogue management.
Data Handling	Xarray	The essential library for working with labeled, multi-dimensional scientific data, specifically designed for formats like NetCDF.
Data Visualization	Plotly	For creating rich, fully interactive, and web-native charts that provide a superior user experience for data exploration.

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

Prerequisites:

    Python 3.9+

    pip package manager

Installation:

    Clone the repository:
    Bash

git clone https://github.com/your_username/FloatChat.git
cd FloatChat

Create and activate a virtual environment:
Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:
Bash

pip install -r requirements.txt

Run the Streamlit application:
Bash

    streamlit run app.py

    The application will now be running on your local machine!

## 🔗 Useful Links

    Live Demo: ``

    ARGO Project: Official ARGO Program Website

    ARGO Data Portal: Euro-Argo Data Selection

```bash
git clone https://github.com/<your-username>/FloatChat-A-Chatbot-for-ARGO.git
cd FloatChat-A-Chatbot-for-ARGO
pip install -r requirements.txt

Run the app:
streamlit run app.py