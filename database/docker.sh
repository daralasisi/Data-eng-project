#!/bin/bash

# Define environment variables
NETWORK_NAME="financial_dashboard_network"
VOLUME_NAME="mysql_data"
CONTAINER_NAME="mysql_financial_dashboard"
MYSQL_ROOT_PASSWORD="rootpassword"
MYSQL_DATABASE="FinancialDashboard"
MYSQL_USER="user"
MYSQL_PASSWORD="userpassword"
DOCKER_COMPOSE_FILE="docker-compose.yml"
SETUP_SQL="setup.sql"

# Check if Docker network exists, if not create it
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Creating Docker network: $NETWORK_NAME"
    docker network create $NETWORK_NAME
else
    echo "Docker network $NETWORK_NAME already exists"
fi

# Check if Docker volume exists, if not create it
if ! docker volume ls | grep -q "$VOLUME_NAME"; then
    echo "Creating Docker volume: $VOLUME_NAME"
    docker volume create $VOLUME_NAME
else
    echo "Docker volume $VOLUME_NAME already exists"
fi

# Create docker-compose.yml file
cat > $DOCKER_COMPOSE_FILE <<EOL

services:
  mysql:
    image: mysql:latest
    container_name: $CONTAINER_NAME
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: $MYSQL_ROOT_PASSWORD
      MYSQL_DATABASE: $MYSQL_DATABASE
      MYSQL_USER: $MYSQL_USER
      MYSQL_PASSWORD: $MYSQL_PASSWORD
    ports:
      - "3306:3306"
    networks:
      - $NETWORK_NAME
    volumes:
      - $VOLUME_NAME:/var/lib/mysql

networks:
  $NETWORK_NAME:
    external: true

volumes:
  $VOLUME_NAME:
    external: true
EOL

# Start MySQL container using docker-compose
echo "Starting MySQL container"
docker-compose up -d

# Wait for the MySQL container to be fully up and running

MAX_TRIES=30
TRIES=0

MAX_TRIES=30
TRIES=0

until docker exec $CONTAINER_NAME mysql -u root -p$MYSQL_ROOT_PASSWORD -e "SELECT 1" &> /dev/null; do
    if [ $TRIES -ge $MAX_TRIES ]; then
        echo "Failed to connect to MySQL after $MAX_TRIES tries"
        exit 1
    fi
    sleep 5
    TRIES=$((TRIES+1))
done

echo "Connected to MySQL successfully"

done

echo "Connected to MySQL successfully"

#check if setup.sql exists
if [ ! -f "$SETUP_SQL"]; then 
     echo "Error: $SETUP_SQL file not found!"
     exit 1
fi

#create the /app directory inside the container
echo 'Creating the /app directory to hold setup.sql'
docker exec $CONTAINER_NAME mkdir /app

# Copy setup.sql to the container
echo "Copying $SETUP_SQL to the MySQL container"
docker cp $SETUP_SQL $CONTAINER_NAME:/app/$SETUP_SQL

# Execute the setup.sql script inside the container
echo "Executing $SETUP_SQL inside the MySQL container"
docker exec -i $CONTAINER_NAME mysql -uroot -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE < /app/setup.sql
echo "MySQL setup complete!"