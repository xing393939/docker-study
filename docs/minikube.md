### minikube相关

#### ubuntu22.04下安装
* [Ubuntu 22.04 Minikube安装配置](https://blog.csdn.net/LeoForBest/article/details/126524892)

```
# 禁用ubuntu自带的dns-server
systemctl stop systemd-resolved
systemctl disable systemd-resolved

# 安装docker
apt install curl
apt install docker.io
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
install minikube-linux-amd64 /usr/local/bin/minikube

# 修改docker的环境
cat /etc/docker/daemon.json
{
  "registry-mirrors" : [
    "https://tycwa26s.mirror.aliyuncs.com"
  ],
  "insecure-registries":["192.168.2.120:5000"],
  "bip": "172.18.0.1/16",
  "dns": ["114.114.114.114", "8.8.8.8"]
}
systemctl restart docker
docker network create --subnet=172.17.0.1/16 minidocker0

# 以下在ubuntu用户下执行
sudo usermod -aG docker $USER && newgrp docker
minikube start --kubernetes-version=v1.23.8 --image-mirror-country=cn --network=minidocker0 --apiserver-ips=192.168.2.120 --insecure-registry=192.168.2.120:5000

# 设置kubectl的alias
vim ~/.bashrc
alias kubectl="minikube kubectl --"
```

#### 配置私有仓库和gitlab
```
docker run -d --network=host --restart=always -p 5000:5000 -v /mnt/registry:/var/lib/registry registry

```
