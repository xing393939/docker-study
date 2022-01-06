### 服务网格

#### 阿里云ASK安装istio
```
# 需先安装coredns插件

# 安装istioctl
curl -L https://istio.io/downloadIstio | sh -

# 安装istio
istioctl manifest generate --set profile=default > istio.yaml
kubectl create ns istio-system
kubectl apply -f istio.yaml

# 安装kiali-先安装prometheus
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.12/samples/addons/prometheus.yaml

# 安装kiali-安装kiali
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.12/samples/addons/kiali.yaml

# 安装bookinfo示例（NET_RAW默认不支持，需提交工单申请：https://help.aliyun.com/document_detail/163023.html）
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.12/samples/bookinfo/platform/kube/bookinfo.yaml
```