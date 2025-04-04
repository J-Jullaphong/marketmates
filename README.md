# MarketMates

MarketMates is an investment community web application that connects investors
through forums, live chat, and private groups. It features expert opinions, 
and daily updates on market conditions. Designed to promote knowledge sharing and market learning,

## Features

- **Community Forums** – Engage in discussions with other investors.
- **Live Chat** – Real-time communication for instant knowledge sharing.
- **Private Groups** – Create or join exclusive groups for focused discussions.
- **Verified Expert Content** – Insights from market experts to guide investment decisions.
- **Daily Market Updates** – Stay informed with real-time data.

---

## Installation Instructions

### Prerequisites

Ensure you have the following installed:

- **Docker & Docker Compose** – [Get Docker](https://www.docker.com/)
- **Git** – [Install Git](https://git-scm.com/)

---

### Development Setup

> **Note:** For this submission, `.env.dev` is already provided — **You can skip step 2 and 3**.

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
    docker compose -f docker-compose-dev.yaml up --build -d
    ```

5. To stop the app:

    ```bash
    docker compose -f docker-compose-dev.yaml down --volumes
    ```

#### Accessing the App (Development)

- **MarketMates App**:
    - URL: [http://localhost:8000/](http://localhost:8000/)

> Monitoring services like Grafana and Prometheus are **not required in development** for faster setup.

---

### Production Setup

> **Note:** For this submission, `.env.prod` is already provided — **You can skip step 2 and 3**.

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

4. Create a Docker network (only once):

    ```bash
    docker network create marketmates
    ```

5. Generate self-signed SSL certificates (or replace with real ones):

    ```bash
    mkdir -p certs
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout certs/nginx-selfsigned.key \
      -out certs/nginx-selfsigned.crt
    ```

6. Create the Grafana secrets for admin login:

    ```bash
    mkdir -p secrets
    echo "admin" > secrets/grafana_admin_user
    echo "your_strong_password_here" > secrets/grafana_admin_password
    ```

7. Start the monitoring stack:

    ```bash
    docker compose -f docker-compose-monitoring.yaml up --build -d
    ```

8. Start the production app:

    ```bash
    docker compose -f docker-compose-prod.yaml up --build -d
    ```

9. To stop everything:

    ```bash
    docker compose -f docker-compose-prod.yaml down --volumes
    docker


#### Accessing the App (Production)

- **MarketMates App**:
    - URL: [https://localhost/](https://localhost/)

- **Grafana Dashboard**:
    - URL: [https://localhost/grafana/](https://localhost/grafana/)
    - Login using the credentials from `secrets/grafana_admin_user`
      and `secrets/grafana_admin_password`

---

## Demo Users

Use these demo accounts to log in for testing.

- **Admin Access** (for Django Admin Panel):  
  - URL: [http://localhost:8000/admin/](http://localhost:8000/admin/) or [https://localhost/admin/](https://localhost/admin/)
  - Login using the **Username** and Password.

- **Normal Users & Experts** (for main app login):  
  - URL: [http://localhost:8000/login/](http://localhost:8000/login/) or [https://localhost/login/](https://localhost/login/)
  - Log in using the **Email** and Password on the main login form.

|       Username       |       Email        |        Password        | 
|:--------------------:|:------------------:|:----------------------:|
|      **admin**       |         -          | marketmates-admin1234  |
|      **demo01**      |  demo01@gmail.com  |     marketmates01      |
|      **demo02**      |  demo02@gmail.com  |     marketmates02      |
| **Expert_NumberOne** | expert01@gmail.com | marketmates-expert1234 |
