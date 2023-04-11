### docker 学习

#### 参考资料
1. [中国区AWS价格计算器](https://cloud.engineerdraft.com/ec2)，按月计算，也计算了预留实例
1. [1.23版本yaml文件字段文档](https://v1-23.docs.kubernetes.io/docs/reference/kubernetes-api/)

#### k8s需要解决的问题
1. pod如何访问外网：[借助宿主机的DNAT和SNAT](https://time.geekbang.org/column/article/11465)
1. cni解决的问题：pod和pod之间的通讯，方案有Flannel和calico
1. kube-proxy：帮助通过clusterIP转发到PodIP，方案有iptables和ipvs
1. kube-dns：帮助通过名称找到指定clusterIP，方案有coreDNS