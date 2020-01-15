eksctl create cluster \
	--kubeconfig "~/.kube/config" \
	--name "flask-redis-api-demo" \
	--nodes 1 \
	--node-type "t2.medium" \
	--region "us-west-2"
