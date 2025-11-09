#!/bin/bash
echo "🐳 Simple Docker Test"
echo "===================="

# Build image
echo "1. Building image..."
docker build -t feature-votes-api:test .

# Check size
echo ""
echo "2. Image size:"
docker images feature-votes-api:test --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Test run with volume for logs
echo ""
echo "3. Testing container (with log volume)..."
docker run -d --name test-app -p 8001:8000 -v $(pwd)/logs:/app/logs feature-votes-api:test
sleep 10

# Check if container is running
echo ""
echo "4. Container status:"
docker ps -f name=test-app

# Check logs
echo ""
echo "5. Container logs:"
docker logs test-app --tail 5

# Health check
echo ""
echo "6. Health check:"
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "   ✅ Application is healthy!"
else
    echo "   ❌ Health check failed"
    echo "   Debug info:"
    docker logs test-app --tail 10
fi

# Cleanup
echo ""
echo "7. Cleaning up..."
docker stop test-app > /dev/null 2>&1
docker rm test-app > /dev/null 2>&1

echo "🎉 Test complete!"