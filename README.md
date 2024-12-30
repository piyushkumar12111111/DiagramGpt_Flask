# Architecture Diagram Generator 🏗️

An AI-powered tool that generates AWS architecture diagrams from natural language descriptions using Python, Flask, Streamlit, and Google's Gemini AI.

![image](https://github.com/user-attachments/assets/a5d50f18-9de1-47bf-ad00-b264de5717e0)


## Features 🌟

- **Natural Language to Diagram**: Convert text descriptions into professional AWS architecture diagrams
- **AI-Powered**: Uses Google's Gemini AI to understand and interpret architectural requirements
- **Interactive UI**: Clean and intuitive Streamlit interface
- **Multiple Components**: Supports various AWS components including:
  - Load Balancers (ALB/ELB)
  - EC2 Instances
  - RDS Databases
  - VPCs and Subnets
  - Security Groups
- **History Tracking**: Keep track of all generated diagrams
- **Export Options**: Download diagrams as PNG files
- **Code View**: See and copy the Python code used to generate diagrams

## Architecture 🏛️

The application follows a microservices architecture:

1. **Frontend**: Streamlit UI for user interaction
2. **Backend**: Flask API for handling requests and business logic
3. **AI Service**: Google Gemini for natural language processing
4. **Diagram Service**: Python Diagrams package for generating architecture diagrams

## Prerequisites 📋

- Python 3.8+
- Graphviz (required for diagram generation)
- Google Gemini API key

## Installation 🚀
