# Persona-Adaptive Customer Support Agent

## Overview

This project is a Persona-Adaptive Customer Support Agent built using Google Gemini, ChromaDB, LangChain, and Streamlit.

The system automatically identifies the customer's communication style, retrieves relevant information from a knowledge base using RAG, and generates responses tailored to the detected persona.

The project demonstrates:

* Persona Classification
* Retrieval-Augmented Generation (RAG)
* Vector Search using ChromaDB
* Adaptive Response Generation
* Human Escalation Workflow
* PDF Knowledge Base Ingestion

## Project Architecture

User Query
↓
Persona Classification (Gemini)
↓
RAG Retrieval (ChromaDB)
↓
Adaptive Prompt Generation
↓
Response Generation (Gemini)
↓
Escalation Check
↓
Human Handoff (if required)

## Technology Stack

* Python 3.11+
* Google Gemini API
* LangChain
* ChromaDB
* Streamlit
* PyPDF
* Python Dotenv

## Project Structure

persona-support-agent/

├── data/
│   ├── account.md
│   ├── coupons.md
│   ├── invoice.txt
|   ├── network.md
│   ├── orders.txt
│   ├── password_reset_guide.pdf
│   ├── payment.md
│   ├── privacy_support.txt
│   ├── refund.md
│   ├── returns.md
│   └── shipping.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── classifier.py
│   ├── rag_pipeline.py
│   ├── generator.py
│   └── escalator.py
│
├── app.py
├── build_index.py
├── requirements.txt
├── README.md
└── .env

## Knowledge Base

The knowledge base contains support documentation related to an e-commerce platform.

Topics include:

* Account Management
* Password Recovery
* Order Tracking
* Shipping Information
* Payment Support
* Refund Processing
* Invoice Management
* Coupons and Discounts
* Product Returns

A PDF document is also included to demonstrate PDF ingestion and retrieval.

## Escalation Rules

The system escalates conversations to a human support agent when:

* Retrieval confidence is below the configured threshold
* Billing or refund related issues are detected
* Legal concerns are mentioned
* Relevant documentation cannot be found

## Installation

### 1. Clone Repository

    bash
git clone <repository-url>
cd persona-support-agent

### 2. Create Virtual Environment

    bash
python -m venv venv

Activate:

Windows

    bash
venv\Scripts\activate

### 3. Install Dependencies

    bash
pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file:

    env
GEMINI_API_KEY=your_api_key_here

## Build Vector Database

Run:

    bash
python build_index.py

This command:

* Loads documents
* Splits documents into chunks
* Generates embeddings
* Stores vectors in ChromaDB

## Run Application

    bash
streamlit run app.py

The application will be available locally through Streamlit.

## Example Queries

### Technical Expert

What are the authentication requirements for login?

### Frustrated User

why i not get free delivery?

### Business Executive

What is the expected timeline for shipping ?

### Escalation Example

I was charged twice and require an immediate refund.

## Future Improvements

* Multi-turn conversation memory
* Sentiment tracking across sessions
* Advanced confidence scoring
* Support ticket integration
* Cloud vector database deployment

## Author

Developed as part of the Persona-Adaptive Customer Support Agent assignment using Google Gemini and Retrieval-Augmented Generation techniques.