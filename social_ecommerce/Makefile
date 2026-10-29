apply:
				kubectl apply -k k8s/

delete:
				kubectl delete -k k8s/

init-db:
				kubectl apply -f k8s/jobs/db-init.yaml

remove-db:
				kubectl delete job db-init-job
