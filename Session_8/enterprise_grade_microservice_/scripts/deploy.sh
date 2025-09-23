```bash
#!/bin/bash

# Set the environment variables
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="YOUR_DEFAULT_REGION"

# Set the Docker image name and tag
IMAGE_NAME="your-service-name"
IMAGE_TAG="latest"

# Set the AWS ECS cluster and service name
ECS_CLUSTER="your-ecs-cluster"
ECS_SERVICE="your-ecs-service"

# Set the AWS ECR repository name
ECR_REPO="your-ecr-repo"

# Set the testing environment variables
TEST_ENVIRONMENT="test"
TEST_IMAGE_NAME="${IMAGE_NAME}-${TEST_ENVIRONMENT}"
TEST_IMAGE_TAG="${IMAGE_TAG}"

# Build the Docker image
echo "Building Docker image..."
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}".

# Push the Docker image to AWS ECR
echo "Pushing Docker image to AWS ECR..."
aws ecr get-login-password --region "${AWS_DEFAULT_REGION}" | docker login --username AWS --password-stdin "${ECR_REPO}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
docker tag "${IMAGE_NAME}:${IMAGE_TAG}" "${ECR_REPO}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
docker push "${ECR_REPO}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"

# Create a new ECS task definition
echo "Creating new ECS task definition..."
aws ecs create-task-definition --family "${IMAGE_NAME}" --requires-compatibilities EC2 --cpu 10 --memory 512 --network-mode awsvpc --container-definitions '[{"name":"${IMAGE_NAME}","image":"${ECR_REPO}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}","portMappings":[{"containerPort":80,"hostPort":80,"protocol":"tcp"}]}]'

# Create a new ECS service
echo "Creating new ECS service..."
aws ecs create-service --cluster "${ECS_CLUSTER}" --service-name "${ECS_SERVICE}" --task-definition "${IMAGE_NAME}" --desired-count 1 --launch-type "EC2"

# Run the tests
echo "Running tests..."
docker build -t "${TEST_IMAGE_NAME}:${TEST_IMAGE_TAG}".
docker run -e "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" -e "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" -e "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" "${TEST_IMAGE_NAME}:${TEST_IMAGE_TAG}"

# Deploy the service
echo "Deploying service..."
aws ecs update-service --cluster "${ECS_CLUSTER}" --service "${ECS_SERVICE}" --task-definition "${IMAGE_NAME}"

# Print the deployment status
echo "Deployment complete."
```