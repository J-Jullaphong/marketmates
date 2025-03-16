# MarketMates

MarketMates is an investment community web application that connects investors through forums, live chat, and private groups. It features expert opinions, actionable market analysis, and daily updates on market conditions. Designed to promote knowledge sharing and market learning, MarketMates fosters a dynamic and engaging environment for investors.

## Features

- **Community Forums** – Engage in discussions with fellow investors.
- **Live Chat** – Real-time communication for instant knowledge sharing.
- **Private Groups** – Create or join exclusive groups for focused discussions.
- **Expert Opinions** – Insights from market experts to guide investment decisions.
- **Market Analysis** – Actionable analysis to help users stay ahead.
- **Daily Market Updates** – Stay informed with real-time data and news.

---

## Installation Instructions

### Prerequisites

Ensure you have the following installed:

- **Docker & Docker Compose** – [Get Docker](https://www.docker.com/)
- **Git** (for cloning the repository) – [Install Git](https://git-scm.com/)

### Development Setup

Follow these steps to set up MarketMates for development:

1. Clone the repository and navigate to the directory:

    ```sh
    git clone https://github.com/your-repo/marketmates.git
    cd marketmates
    ```

2. Copy the sample environment file:

   ```sh
   cp sample.env .env.dev
   ```

3. Set the environment variables within `.env.dev`.

4. Start the application using Docker Compose:

   ```sh
   docker-compose -f docker-compose-dev.yaml up --build
   ```

5. To stop the application:

   ```sh
   docker-compose -f docker-compose-dev.yaml down
   ```

---

### Production Setup

To deploy MarketMates in a production environment:

1. Clone the repository and navigate to the directory:

    ```sh
    git clone https://github.com/your-repo/marketmates.git
    cd marketmates
    ```

2. Copy the sample environment file:

   ```sh
   cp sample.env .env.prod
   ```

3. Set the environment variables within `.env.prod`.

4. Generate SSL certificates:

   ```sh
   mkdir -p certs
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
   -keyout certs/nginx-selfsigned.key \
   -out certs/nginx-selfsigned.crt
   ```

5. Start the application using Docker Compose:

   ```sh
   docker-compose -f docker-compose-prod.yaml up --build -d
   ```

6. To stop the application:

   ```sh
   docker-compose -f docker-compose-prod.yaml down
   ```

---

## Usage

Once the application is running, you can access it via:

- HTTP: http://localhost:8000/
- HTTPS: https://localhost/

If you are running it in a production environment with a domain, replace localhost with your domain.
