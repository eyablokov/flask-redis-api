docker login

cd service
docker build -t ${DOCKER_HUB_USER}/service .
cd ..
