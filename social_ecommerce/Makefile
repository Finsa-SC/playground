up:
				@printf "\nCreating Persistent Volume Claim..."
				kubectl apply -k k8s/storage/
				@printf "\nApplying k8s..."				
				kubectl apply -k k8s/app/db
				kubectl apply -k k8s/app/api
				kubectl apply -k k8s/app/proxy


down:
				
				kubectl delete -k k8s/app/db
				kubectl delete -k k8s/app/api
				kubectl delete -k k8s/app/proxy

get:
				kubectl get pods

up-proxy:
				kubectl apply -k k8s/app/proxy/

down-proxy:
				kubectl delete -k k8s/app/proxy/

restart-proxy:
				kubectl delete -k k8s/app/proxy/
				kubectl apply -k k8s/app/proxy/

				
init-db:
				@printf "\nCleaning up previous db job..."
				kubectl delete job db-init-job
				@printf "\nCreating db init job..."
				kubectl apply -f k8s/jobs/db-init.yaml

seed-db:
				kubectl apply -f k8s/jobs/db-seed.yaml
