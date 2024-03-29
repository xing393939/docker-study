### Kubernetes 基础

#### 参考资料
1. [kubernetes handbook](https://jimmysong.io/kubernetes-handbook/concepts/objects.html)，k8s的资源对象
1. [kubernetes ingress+traefik](http://www.showerlee.com/archives/2701)
1. [k3s 配置 traefik web-ui](https://www.jianshu.com/p/0040e8bd6d1e)
1. [视频，k3s进阶之路](https://space.bilibili.com/430496045/channel/detail?cid=103026)

#### k8s 四种 service 类型
1. [以图形化的方式简单介绍 Kubernetes Service](https://blog.csdn.net/qq_36441027/article/details/104209807)
1. ClusterIP 是最基础的。集群内部可见。
1. 创建一个 NodePort 类型的 service，Kubernetes 会创建 ClusterIP。外部可见。
1. 创建一个 LoadBalance 类型的 service，Kubernetes 会创建 NodePort、ClusterIP。
1. ExternalName 类型不常用

#### 多集群、多命名空间的管理
1. [kubernetes 中 kubeconfig 的用法](https://www.jianshu.com/p/99853cac56b8)
1. vim ~/.kube/config，修改认证配置
1. kubectl config get-contexts，获取所有的认证配置
1. kubectl config use-context kube2，切换到配置名=kube2上
1. kubectl config rename-context old new，修改配置名

```
# 设置 KUBECONFIG 的环境变量
export KUBECONFIG=/etc/kubernetes/kubeconfig/kubelet.kubeconfig
# 指定 kubeconfig 文件
kubectl get node --kubeconfig=/etc/kubernetes/kubeconfig/kubelet.kubeconfig
# 使用不同的 context 在多个集群之间切换
kubectl get node --kubeconfig=./kubeconfig --context=cluster1-context 
```

#### k3s 的一些问题：
1. 容器的运行环境：docker或者containerd(cri)。k3s默认的容器环境是containerd。
1. k3s指定容器用docker：
  * curl https://releases.rancher.com/install-docker/19.03.sh | sh
  * curl -sfL http://rancher-mirror.cnrancher.com/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -s - --docker
1. 启动后netstat 看不到80、443端口：nmap -sT -p 80 localhost
1. 清理没有用到的镜像：k3s crictl rmi --prune
1. 国内安装脚本：curl -sfL https://docs.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -
1. 国内修改镜像源：vim /etc/rancher/k3s/registries.yaml 并重启 systemctl restart k3s
```
mirrors:
  "docker.io":
    endpoint:
      - "https://fogjl973.mirror.aliyuncs.com"
      - "https://registry-1.docker.io"
```

#### k3s 集群搭建
```
# 方法一，安装时指定master
curl -sfL http://rancher-mirror.cnrancher.com/k3s/k3s-install.sh | INSTALL_K3S_EXEC="--node-external-ip=0.0.0.0" sh -s -
curl -sfL http://rancher-mirror.cnrancher.com/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn K3S_URL=https://myserver:6443 K3S_TOKEN=${NODE_TOKEN} sh -

# 方法二，先安装，再指定master
curl -sfL http://rancher-mirror.cnrancher.com/k3s/k3s-install.sh | INSTALL_K3S_EXEC="--node-external-ip=0.0.0.0" sh -s -

k3s agent --server https://myserver:6443 --token ${NODE_TOKEN}
```

#### k8s 的基础命令：
1. [如何成功通过 CKA 考试](https://www.zhaohuabing.com/post/2021-12-20-how-to-prepare-cka/)
1. yaml文件字段参考：https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/
1. kubectl get pod //查看pod，加上-o wide可以获取更多列信息
1. kubectl get node //查看node
1. kubectl get all -n kube-system //查看所有kube-system空间的资源
1. kubectl edit configmap traefik -n kube-system   //修改configMap
1. kubectl delete pod traefik-758cd5fc85-smvd9     //删除pod（将自动重启一个新的）
1. kubectl explain pod.spec.containers //查看yaml文件containers的配置说明
1. kubectl run --help | head -n 30 //有大量创建pod的示例
1. kubectl get pod | jq .items[].metadata.name //用jq来提取详细信息
1. [k8s args和command](https://www.e-learn.cn/topic/3101694)
  * docker的entrypoint、cmd对应容器的command、args

#### kubernetes 使用私有仓库
1. [k8s拉取私库镜像](https://developer.aliyun.com/article/746670)
1. 使用阿里云：https://cr.console.aliyun.com/us-east-1/instances/credentials
1. 使用阿里云：https://www.cnblogs.com/weifeng1463/p/10063208.html
1. 先创建secret卷，在yaml配置imagePullSecrets.name=secret卷名

#### 如何判断容器环境是docker还是lxc
1. [如何检测该服务器使用的是Container技术还是VM技术](http://dockone.io/question/171)
1. [Golang 如何确定App是否运行在Docker内](http://chen-tao.github.io/2017/09/11/Go-check-if-app-running-in-docker/)
1. docker 如何进入容器：docker exec -it 容器id /bin/bash
1. kubectl 如何进入容器：kubectl exec -it {pod id} -- /bin/bash
1. 容器内cat /proc/1/cgroup # 包含docker
1. 容器内ls /.dockerenv     # 如果有就是docker

#### kubernetes判断cri是docker还是containerd
1. 通过kubectl describe node命令查看Container Runtime Version项可以得知
1. 通过kubectl describe pod命令查看Container ID项可以得知
1. 容器内cat /proc/1/cgroup # 包含docker就是docker，包含kubepods可能是containerd
