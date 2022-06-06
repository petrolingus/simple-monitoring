# Simple Monitoring

Lightweight python application for collect metrics from apps running in kubernetes

## Requirements

 * Kubernetes >= 1.23.0
 * Python >= 3.9

## How to use this

### Creating RBAC

The kubernetes folder contains the cluster-role-binding.yaml and service-account.yaml files,
each of which must be applied to the cluster.

```txt
    kubectl apply -f cluster-role-binding.yaml
    kubectl apply -f service-account.yaml
    kubectl get secrets -n kube-system | grep simple-monitoring-admin-token
    kubectl describe secret <your-secret-name> -n kube-system
```

### Change kube-config

 You need to set valid cluster server and user token in kube-config file
 
### Just run it

```angular2html
python3 main.py
```