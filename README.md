# MarketMates

MarketMates is an investment community web application that connects investors through forums, live chat, and private groups. It features expert opinions, actionable market analysis, and daily updates on market conditions. Designed to promote knowledge sharing and market learning, MarketMates fosters a dynamic and engaging environment for investors.

## Features

- **Community Forums** – Engage in discussions with fellow investors.
- **Live Chat** – Real-time communication for instant knowledge sharing.
- **Private Groups** – Create or join exclusive groups for focused discussions.
- **Expert Opinions** – Insights from market experts to guide investment decisions.
- **Market Analysis** – Actionable analysis to help users stay ahead.
- **Daily Market Updates** – Stay informed with real-time data.

---

## Installation Instructions

### Prerequisites

Ensure you have the following installed:

- **Docker & Docker Compose** – [Get Docker](https://www.docker.com/)
- **Git** – [Install Git](https://git-scm.com/)

---

### Development Setup

1. Clone the repository and navigate to the directory:

    ```bash
    git clone https://github.com/J-Jullaphong/marketmates.git
    cd marketmates
    ```

2. Copy the sample environment file:

    ```bash
    cp sample.env .env.dev
    ```

3. Set the environment variables inside `.env.dev`.

4. Start the development app:

    ```bash
    docker-compose -f docker-compose-dev.yaml up --build
    ```

5. To stop the app:

    ```bash
    docker-compose -f docker-compose-dev.yaml down --volumes
    ```
   
#### Accessing the App (Development)

- **MarketMates App**:  
  - URL: [http://localhost:8000/](http://localhost:8000/)

> Monitoring services like Grafana and Prometheus are **not required in development** for faster setup.

---

### Production Setup

1. Clone the repository and navigate to the directory:

    ```bash
    git clone https://github.com/J-Jullaphong/marketmates.git
    cd marketmates
    ```

2. Copy the sample environment file:

    ```bash
    cp sample.env .env.prod
    ```

3. Set your production environment variables inside `.env.prod`.

4. Generate self-signed SSL certificates (or replace with real ones):

    ```bash
    mkdir -p certs
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout certs/nginx-selfsigned.key \
      -out certs/nginx-selfsigned.crt
    ```

5. Create the Grafana secrets for admin login:

    ```bash
    mkdir -p secrets
    echo "admin" > secrets/grafana_admin_user
    echo "your_strong_password_here" > secrets/grafana_admin_password
    ```

6. Start the monitoring stack:

    ```bash
    docker-compose -f docker-compose-monitoring.yaml up --build -d
    ```
   
7. Start the production app:

    ```bash
    docker-compose -f docker-compose-prod.yaml up --build -d
    ```

8. To stop everything:

    ```bash
    docker-compose -f docker-compose-prod.yaml down --volumes
    docker-compose -f docker-compose-monitoring.yaml down --volumes
    ```

#### Accessing the App (Production)

- **MarketMates App**:  
  - URL: [https://localhost/](https://localhost/)

- **Grafana Dashboard**:  
  - URL: [https://localhost/grafana/](https://localhost/grafana/)  
  - Login using the credentials from `secrets/grafana_admin_user` and `secrets/grafana_admin_password`