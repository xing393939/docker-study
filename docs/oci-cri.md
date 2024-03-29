### oci开放容器标准和cri容器运行时标准

#### 几个术语
1. [docker 的功能组件与结构](https://blog.laisky.com/p/docker-component/)
1. [K8S Runtime CRI OCI contained dockershim 理解（转）](https://www.cnblogs.com/charlieroro/articles/10998203.html)
1. OCI：Open Container Initiative，容器运行标准，分为Image Specification和Runtime Specification
  1. Image Specification：压缩的文件夹，文件夹里以 xxx 结构放 xxx 文件
  1. Runtime Specification：能接收哪些指令（create、start、stop），这些指令的行为是什么
1. CRI：Container Runtime Interface，容器运行时标准，k8s的1.5+开始使用
  1. [cri-o](https://cri-o.io/): 支持 CRI 的轻量级 container runtime；
  1. [rktlet](https://github.com/kubernetes-incubator/rktlet)：支持 rtk 的 CRI（rkt 不支持 OCI）；
  1. [cri-containerd](https://github.com/containerd/cri)：支持 containerd 的 CRI。
1. CNM：Container Network Model，容器网络模型，docker公司提出的概念
  1. libnetwork，Docker公司的，默认支持的driver有None、Bridge、Overlay
  1. CNI，CoreOS公司的，k8s采用了
1. CNI：Container Network Interface，容器网络标准，对应是实现有calico、Flannel
1. IPAM: IP address management，IP 地址管理工具，如 DHCP 或 DNS

#### k8s解耦docker依赖的过程
1. [开放容器标准OCI内部分享](https://xuanwo.io/2019/08/06/oci-intro/)
1. cri -> dockershim
1. cri -> cri-containerd -> containerd
1. cri -> containerd（内置cri-containerd），要求Kubernetes>=1.10，pod的启动延迟、CPU、内存占用率都得到优化

#### Low-Level 和 High-Level 容器运行时
1. [容器运行时 1 - 容器运行时简介](http://liupeng0518.github.io/2019/10/06/docker/runtimes/Container%20Runtimes%20Part%201/)
1. 容器是使用Linux namespaces和cgroups实现的
1. Low-Level 和 High-Level 是另一种容器分类的角度。实际上使用low-level runtimes 的只有那些实现High-Level runtimes的开发人员
1. containerd和cri-o实际上使用runc来运行容器。runc是low-level容器，containerd和cri-o是High-Level容器
1. rkt容器即实现了low-level也实现了High-Level

#### 工具
1. containers/buildah：目标是构建 OCI 容器镜像，Daemon free，支持 Rootless 构建
1. containers/skopeo：可以在不用下载到本地的前提下查看远端 Registry 中的镜像信息
1. containers/libpod：二进制名为 podman，支持管理 Pod，容器，镜像和存储卷（镜像部分的代码主要使用了 buildah）
1. genuinetools/img：支持Dockerfile构建，支持推送到仓库，不支持运行容器

#### rkt和LXD/LXC
1. [白话 Kubernetes Runtime](https://aleiwu.com/post/cncf-runtime-landscape/)
1. [Docker、LXC、LXD这三种容器的区别](https://blog.csdn.net/zhengmx100/article/details/79415742)
1. rkt跟docker一样是容器化应用程序，特点是无daemon，目前项目基本不活跃了
1. LXD可以视作LXC的升级版，LXD的目标是容器化操作系统，背后是Ubuntu公司












