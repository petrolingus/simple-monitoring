import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from kubernetes import client
from kubernetes import config
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
config.load_kube_config(config_file='kube-config')


@app.get("/get_all_pods")
def get_all_pods():
    api_client = client.ApiClient()
    api_instance = client.CoreV1Api(api_client)
    api_response = api_instance.list_pod_for_all_namespaces(watch=False)
    pods = {}
    for pod in api_response.items:
        if pod.metadata.annotations and pod.metadata.annotations.get('prometheus.io/scrape'):
            namespace = pod.metadata.namespace
            port = pod.metadata.annotations.get('prometheus.io/port')
            path = pod.metadata.annotations.get('prometheus.io/path')
            pods[pod.metadata.name] = {'namespace': namespace, 'metrics_port': port, 'metrics_path': path}
    json_result = json.dumps(pods, indent=4)
    print(json_result)
    return json_result


@app.get("/get_metrics/")
def get_metrics(pod_name: str, pod_port: str, namespace: str, metrics_path: str):
    api_client = client.CoreV1Api()
    name = pod_name + ':' + pod_port
    res = api_client.connect_get_namespaced_pod_proxy_with_path(name, namespace, metrics_path, _preload_content=False)
    result = res.data.decode("utf-8").split('\n')
    return json.dumps(result, indent=4)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
