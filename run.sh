#!/bin/bash

cd kubernetes

kubectl delete deployment simple-monitoring -n monitoring
kubectl apply -f deployment.yaml -n monitoring
#kubectl apply -f ./dir