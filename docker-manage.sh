#!/bin/bash

# Docker management script for Kirana AI Streamlit app

case "$1" in
    "start")
        echo "Starting Kirana AI Streamlit app..."
        docker-compose up -d
        echo "App started! Visit http://localhost:8501"
        ;;
    "stop")
        echo "Stopping Kirana AI Streamlit app..."
        docker-compose down
        ;;
    "restart")
        echo "Restarting Kirana AI Streamlit app..."
        docker-compose down
        docker-compose up -d
        echo "App restarted! Visit http://localhost:8501"
        ;;
    "logs")
        echo "Showing logs..."
        docker-compose logs -f streamlit-app
        ;;
    "status")
        echo "Checking status..."
        docker-compose ps
        ;;
    "build")
        echo "Building Docker image..."
        docker build -t kirana-ai-streamlit .
        ;;
    "rebuild")
        echo "Rebuilding and restarting..."
        docker-compose down
        docker build -t kirana-ai-streamlit .
        docker-compose up -d
        echo "App rebuilt and restarted! Visit http://localhost:8501"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|status|build|rebuild}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the Streamlit app"
        echo "  stop     - Stop the Streamlit app"
        echo "  restart  - Restart the Streamlit app"
        echo "  logs     - Show app logs"
        echo "  status   - Show container status"
        echo "  build    - Build Docker image"
        echo "  rebuild  - Rebuild image and restart app"
        exit 1
        ;;
esac
