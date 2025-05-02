# Tiajuda API

A Flask-based API for managing IT support tickets with GLPI integration.

## Overview

Tiajuda API is a RESTful service that facilitates the creation and management of IT support tickets. It integrates with GLPI to provide a seamless ticketing system while maintaining its own database for tracking and analytics.

# Context this API was created for
This API was developed for a company that uses GLPI Service integrated with Active Directory users.
The main purpose of this API is to be integrated with a Desktop Application where users can open Tickets more easily than using GLPI Web Interface.
(My interface was built using CustomTkinter, but it can be implemented with any framework or language you prefer)

## Features

- RESTful API endpoints for ticket management
- Integration with GLPI ticketing system
- Rate limiting and IP filtering for security
- MySQL database for ticket storage
- MongoDB for rate limiting storage
- Environment-based configuration

## Prerequisites

- Python 3.x
- MySQL Server
- MongoDB Server
- GLPI instance with API access

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd tiajuda_api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```env
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=your_mysql_host
MYSQL_DATABASE=your_mysql_database
MONGODB_HOST=your_mongodb_host
MONGODB_PORT=your_mongodb_port
MONGODB_DATABASE=your_mongodb_database
WHITELIST_IPS=comma,separated,ip,addresses
```

## Project Structure

```
tiajuda_api/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── ticket.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── newticket.py
│   ├── __init__.py
│   ├── extensions.py
│   └── glpi_api.py
├── venv/
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```

## Models

### Ticket Model

The `Ticket` model represents a support ticket in the system with the following fields:

- `id` (Integer, Primary Key): Unique identifier for the ticket
- `ticket_title` (String): Title of the support ticket
- `requester_username` (String): Username of the person requesting support
- `requester_fullname` (String): Full name of the requester
- `department` (String): Department of the requester
- `anydesk` (String): AnyDesk ID for remote support
- `computer_name` (String): Name of the computer requiring support
- `creation_datetime` (DateTime): Timestamp of ticket creation
- `user_glpi_id` (Integer): GLPI user ID
- `ticket_glpi_id` (Integer): GLPI ticket ID
- `requester_ip` (String): IP address of the requester

## Routes

### New Ticket Endpoint

**Endpoint:** `/api/newticket`

**Method:** POST

**Rate Limit:** 5 requests per 10 minutes, 20 requests per hour

**Request Body:**
```json
{
    "ticket_title": "string",
    "requester_username": "string", #if invalid username provided, logged_username will be used
    "department": "string",
    "anydesk": "string",
    "computer_name": "string",
    "logged_username": "string"
}
```

**Response:**
- Success (201): Returns the created ticket information
- Error (400): Returns error details if required fields are missing or if there's an issue creating the ticket
- Error (429): Excedeed request limit
- Error (403): Invalid IP's

## Security Features

- Rate limiting using Flask-Limiter
- IP whitelisting
- Environment variable configuration
- Database transaction management
- Error handling and logging

## Dependencies

- Flask 3.0.2
- Flask-SQLAlchemy 3.1.1
- Flask-Limiter 3.5.0
- Flask-IPFilter 0.0.5
- python-dotenv 1.0.1
- requests 2.31.0
- PyMySQL 1.1.0
- pymongo 4.6.1
- ipaddress 1.0.23

## Running the Application

1. Ensure all environment variables are set in the `.env` file
2. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:1206` by default.

