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

## Setup and Installation

To run this project locally, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/WojciechMierzwa/RealEstateWebScraper.git
    cd RealEstateWebScraper
    ```

2. **Ensure Docker is installed** on your machine. If not, install it from [here](https://docs.docker.com/get-docker/).

3. **Build and run the services** using Docker Compose:

    ```bash
    docker-compose up --build
    ```

4. **Access the web interface**:
   - The web service will be available at: [http://localhost:5000](http://localhost:5000).
   - The MongoDB service will be running on port 27017.

## Interface Details

- **Main Page**: Shows a basic interface for filtering real estate listings.
- **Scrape Page**: Allows you to trigger the scraper, which fetches the latest property listings from portel.pl.

## Libraries Used

- **Flask**: For building the web interface.
- **pymongo**: To interact with MongoDB for filtering and querying.
- **re (Regular Expressions)**: To clean and format data (especially price data).
- **BeautifulSoup**: To parse HTML and extract relevant data from the site.

## Engine Functionality

The engine is responsible for:

1. **Fetching HTML data** from portel.pl using `requests`.
2. **Parsing the HTML** using `BeautifulSoup` to extract property data.
3. **Storing the extracted data** in MongoDB.
4. **Running the scraper asynchronously**, allowing it to handle multiple pages without blocking the program.

## Docker Containers

The project consists of three Docker containers:

- **Web**: Hosts the Flask application on port 5000.
- **Engine**: Runs the scraping logic and saves data to MongoDB.
- **MongoDB**: Database running on port 27017 for data storage.

## Future Improvements

- **Implement more advanced filtering and sorting** options for users.
- **Enhance error handling** in the scraping process.
- **Improve UI design** for a better user experience.
- **Implement user authentication** for added security.

## Author

- **Name**: Wojciech Mierzwa


