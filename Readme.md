
---

# Api-DNI

A Flask-based application that interacts with the ApisNetPe API to fetch and manage data using Peruvian DNI. This project is containerized with Docker for easy deployment and management.

## 🚀 Getting Started

### Prerequisites

Make sure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Gutierrez-16/Api-DNI.git
   cd Api-DNI
   ```

2. **Create a `.env` File**

   In the root directory of the project, create a file named `.env` and add the following line:

   ```env
   API_TOKEN=your_api_token_here
   ```

   Replace `your_api_token_here` with your actual API token.

3. **Build and Start the Application**

   Use Docker Compose to build and run the application:

   ```bash
   docker-compose up --build
   ```

4. **Access the Application**

   Open your browser and navigate to [http://localhost:5000](http://localhost:5000) to view the application.



