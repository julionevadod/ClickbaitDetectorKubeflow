cat <<EOF | kind create cluster --name=kubeflow  --kubeconfig mycluster.yaml --config=-                                                  
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  image: kindest/node:v1.29.4
  kubeadmConfigPatches:
  - |
    kind: ClusterConfiguration
    apiServer:
      extraArgs:
        "service-account-issuer": "kubernetes.default.svc"
        "service-account-signing-key-file": "/etc/kubernetes/pki/sa.key"
EOF
kind get kubeconfig --name kubeflow > ~/.kube/config
docker login
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=/Users/julionevado/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson