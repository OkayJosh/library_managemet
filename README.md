## Instructions

### Step 1: Set Execute Permission

Run the following command to set execute permissions on the PostgreSQL provisioning script:

```bash
chmod +x docker/provision/postgresql/create-multiple-postgresql-databases.sh
```

### Step 2: Modify Directory Permissions
```bash 
sudo chmod -R 775 .
```

### Step 3: Copy Environment Files
```bash
cp .env.example .env
```
```bash
cp .env.second.example .env.second
```

### Step 4: Build the Containers
```bash
docker build -t lb:latest .
```
```bash
docker build -f postgres.Dockerfile -t lb-postgres .
```

### Step 5: Start and Stop the Application
```bash
docker compose up
```

```bash
docker compose down
```

### Usage Resources
* Environment variable for API calls: [ENV API](http-client.env.json)
* List of API calls: [API CALLS](library_management.http)
