### minikube相关

#### ubuntu22.04下安装
```
# 参考：https://blog.csdn.net/LeoForBest/article/details/126524892
apt install curl
apt install docker.io
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
install minikube-linux-amd64 /usr/local/bin/minikube
# 以下在ubuntu用户下执行
sudo usermod -aG docker $USER && newgrp docker
minikube start --kubernetes-version=v1.23.8 --image-mirror-country=cn --registry-mirror='https://tycwa26s.mirror.aliyuncs.com'
# 设置kubectl的alias
vim ~/.bashrc
alias kubectl="minikube kubectl --"


```

