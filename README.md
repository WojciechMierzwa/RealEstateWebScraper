# RealEstateWebScraper: Web Scraping with Flask and MongoDB

## Project Overview

This project focuses on building a web scraper that gathers real estate listings from [portel.pl](https://www.portel.pl). The scraper is designed to bypass promoted ads and extract valuable property listings starting from the 5th entry on each page. The data is filtered and stored in a MongoDB database, and users can interact with the data via a Flask-based web interface. Sorting and filtering options are available through MongoDB queries, enhancing the user experience.

## Features
- **Web Scraping**: Extract property listings from portel.pl, including specifications, price, contact information, date of posting, and images.
- **MongoDB Storage**: Efficiently stores scraped data in MongoDB for easy access and querying.
- **Flask Web Interface**: Provides a simple web interface for viewing and interacting with the data, including filters and sorting functionalities.
- **Asynchronous Processing**: Uses asynchronous operations for scraping and storing data, improving performance.
- **Dockerized Setup**: The entire project is containerized for easy setup and deployment.

## Technology Stack
- **Flask**: Web framework for the user interface.
- **MongoDB**: NoSQL database to store and manage property listings.
- **BeautifulSoup & Requests**: Python libraries for web scraping.
- **Docker**: Used for containerizing the application.
- **pymongo**: Python client for interacting with MongoDB.

## Repository Structure
The repository is organized into three services:
- **Web (Flask)**: Hosts the web application on port 5000.
- **Engine (Scraper)**: Scrapes data from the website and sends it to the MongoDB database.
- **MongoDB**: Database for storing scraped property listings.


