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
  "insecure-registries": ["192.168.2.120:5000"],
  "bip": "172.18.0.1/16",
  "dns": ["114.114.114.114", "8.8.8.8"]
}
systemctl restart docker
docker network create --subnet=172.17.0.1/16 minidocker0

# 以下在ubuntu用户下执行
sudo usermod -aG docker $USER && newgrp docker
minikube start --kubernetes-version=v1.23.8 --image-mirror-country=cn --network=minidocker0 --apiserver-ips=192.168.2.120 --insecure-registry=192.168.2.120:5000 --addons=ingress

# 设置kubectl的alias
vim ~/.bashrc
alias kubectl="minikube kubectl --"
```

#### 配置私有仓库和ingress组件
```
# 私有仓库
docker run -d --network=host --restart=always -p 5000:5000 -v /mnt/registry:/var/lib/registry registry

# ingress组件只能在minikube start的时候配置代理安装
export HTTP_PROXY=http://192.168.3.119:10809
export HTTPS_PROXY=http://192.168.3.119:10809
export NO_PROXY=localhost,127.0.0.1,192.168.0.1/16,10.96.0.0/12,172.16.0.1/12
# ingress组件minikube start安装好后，重置下环境变量
export HTTP_PROXY=
export HTTPS_PROXY=
export NO_PROXY=

# ingress组件其他安装方案
1. 翻墙pull镜像，导出再导入到minikube环境：https://www.liujiajia.me/2022/5/28/manual-import-image-to-minikube
2. minikube ssh进入，找到 /etc/kubernetes/addons/ingress-deploy.yaml
3. 修改此yaml文件去掉镜像的sha265值，直接kubectl apply
```

#### 简单示例
```
kubectl create deployment hello-minikube1 --image=192.168.2.120:5000/test/node-server:v2
kubectl expose deployment hello-minikube1 --type=ClusterIP --port=8082
kubectl patch configmap tcp-services -n ingress-nginx --patch '{"data":{"8082":"service/hello-minikube2:8082"}}'
```

#### 配置mysql
```
docker run -d -e MYSQL_ROOT_PASSWORD=123456 -v /mnt/mysql-conf:/etc/mysql/conf.d -v /mnt/mysql:/var/lib/mysql --network host --name mysql -p 3306:3306 --restart always mysql:5.7.32

# 参考：https://www.cnblogs.com/bianxj/articles/9567370.html

# 配置文件：/mnt/mysql-conf/config-file.cnf
[mysqld]
port            = 3306
gtid_mode=on
enforce_gtid_consistency=on
server_id=87
binlog_format=row
log-slave-updates=1
replicate-do-db=gozero

# 操作命令
stop slave;
reset slave;
reset master;
set @@global.gtid_purged='xxx,
xxx';
change master to master_host='xxx.rds.aliyuncs.com', master_port=3306, master_user='xxx', master_password='xxx', master_auto_position=1;
start slave;
```