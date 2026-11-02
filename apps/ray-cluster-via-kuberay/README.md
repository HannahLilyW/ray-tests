# Ray Cluster Quickstart

From https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#kuberay-raycluster-quickstart

## 0. Preparation
Install kubectl (>= 1.23), Helm (>= v3.4) if needed, Kind, and Docker.

Make sure your Kubernetes cluster has at least 4 CPU and 4 GB RAM.

## 1. Create a Kubernetes cluster

This step creates a local Kubernetes cluster using Kind. If you already have a Kubernetes cluster, you can skip this step.

`kind create cluster --image=kindest/node:v1.26.0`

## 2. Deploy a KubeRay operator

Install Kuberay Operator via Helm by running the following:

```
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
kubectl create namespace ray-system
helm install kuberay-operator kuberay/kuberay-operator --version 1.7.0 -n ray-system
```

The above installs the operator into a dedicated ray-system namespace rather than default to isolate the operator’s service account from workload pods.

See that the operator is running with `kubectl get pods -n kuberay-system`

## 3. Deploy a RayCluster custom resource

The following installs a sample RayCluster CR in the default namespace:

`helm install raycluster kuberay/ray-cluster --version 1.7.0`

See it with `kubectl get rayclusters`

The KubeRay operator from step 2 detects the RayCluster object and starts your Ray cluster by creating head and worker pods. To view the Ray cluster's pods, run `kubectl get pods --selector=ray.io/cluster=raycluster-kuberay`

## 4. Run an application on a RayCluster

2 methods of doing this:

### Method 1: Execute a ray job in the head pod

The following executes a job which prints cluster resources:

```
export HEAD_POD=$(kubectl get pods --selector=ray.io/node-type=head -o custom-columns=POD:metadata.name --no-headers)
echo $HEAD_POD
kubectl exec -it $HEAD_POD -- python -c "import ray; ray.init(); print(ray.cluster_resources())"
```

### Method 2: Submit a job using ray job submission SDK

1. Port forward the dashboard service with `kubectl port-forward svc/raycluster-kuberay-head-svc 8265:8265`
2. `ray job submit --address http://localhost:8265 -- python -c "import ray; ray.init(); print(ray.cluster_resources())"`

## 5. Access ray dashboard

1. Port forward the dashboard service with `kubectl port-forward svc/raycluster-kuberay-head-svc 8265:8265`
2. Access localhost:8265 in browser

## 6. Cleanup

If you have any port forwards running in background, `killall kubectl`

`kind delete cluster`

# Ray Core

From https://docs.ray.io/en/latest/ray-core/walkthrough.html

Once cluster is up using steps above,

```
cd apps/ray-cluster-via-kuberay
ray job submit --address http://localhost:8625 --working-dir . -- python square.py
```