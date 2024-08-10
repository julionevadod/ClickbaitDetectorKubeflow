# Configuration
1. Install Kubeflow Pipelines
2. Launch Kubeflow pipelines
3. Install Training Operator
    - kubectl apply -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=v1.7.0"
    - kubectl apply -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=master"
4. Launch PytorchJob k8s Object