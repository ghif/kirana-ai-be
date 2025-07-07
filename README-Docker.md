# Kirana AI Streamlit App - Docker Deployment

This directory contains the Docker configuration for deploying the Kirana AI Streamlit application.

## Prerequisites

- Docker Desktop installed and running
- At least 2GB of available RAM
- Port 8501 available on your system

## Quick Start

### Using Docker Compose (Recommended)

1. **Start the application:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   Open your browser and navigate to: http://localhost:8501

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Using the Management Script

A convenience script is provided for easy management:

```bash
# Start the app
./docker-manage.sh start

# Stop the app
./docker-manage.sh stop

# Restart the app
./docker-manage.sh restart

# View logs
./docker-manage.sh logs

# Check status
./docker-manage.sh status

# Rebuild and restart
./docker-manage.sh rebuild
```

### Using Docker Commands Directly

1. **Build the image:**
   ```bash
   docker build -t kirana-ai-streamlit .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8501:8501 --name kirana-ai-streamlit kirana-ai-streamlit
   ```

3. **Stop and remove the container:**
   ```bash
   docker stop kirana-ai-streamlit
   docker rm kirana-ai-streamlit
   ```

## Configuration

### Environment Variables

The application uses the following environment variables:
- `PYTHONPATH=/app` - Set automatically in the container

### Port Configuration

- **Container Port:** 8501 (Streamlit default)
- **Host Port:** 8501 (mapped to localhost:8501)

To use a different host port, modify the `docker-compose.yml` file:
```yaml
ports:
  - "YOUR_PORT:8501"
```

## Health Checks

The container includes health checks that verify the application is running correctly:
- **Health Check URL:** http://localhost:8501/_stcore/health
- **Check Interval:** 30 seconds
- **Timeout:** 10 seconds
- **Retries:** 3

## Development

### Volume Mounting for Development

To enable live code reloading during development, uncomment the volumes section in `docker-compose.yml`:

```yaml
volumes:
  - .:/app
```

This will mount your local directory into the container, allowing you to see changes without rebuilding.

### Logs and Debugging

View application logs:
```bash
docker-compose logs -f streamlit-app
```

Access the container shell:
```bash
docker exec -it kirana-ai-streamlit /bin/bash
```

## File Structure

```
├── Dockerfile              # Container definition
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Files to exclude from build context
├── docker-manage.sh        # Management script
├── requirements.txt        # Python dependencies
└── app.py                 # Main Streamlit application
```

## Troubleshooting

### Port Already in Use
If port 8501 is already in use:
1. Stop any running Streamlit processes: `pkill -f streamlit`
2. Or modify the port in `docker-compose.yml`

### Container Won't Start
1. Check logs: `docker-compose logs streamlit-app`
2. Verify Docker Desktop is running
3. Ensure sufficient system resources

### Application Not Loading
1. Wait for the health check to pass (may take 30-60 seconds)
2. Check container status: `docker-compose ps`
3. Verify the application is accessible: `curl http://localhost:8501`

## Performance

- **Memory Usage:** ~500MB-1GB depending on loaded models
- **CPU Usage:** Moderate, scales with concurrent users
- **Startup Time:** 30-60 seconds for full initialization

## Security

- The container runs with non-root user privileges
- Only port 8501 is exposed
- No sensitive data is included in the image
- Environment variables should be used for secrets (not hardcoded)

## Updates

To update the application:
1. Pull the latest code
2. Rebuild and restart: `./docker-manage.sh rebuild`

Or manually:
```bash
docker-compose down
docker build -t kirana-ai-streamlit .
docker-compose up -d
```
