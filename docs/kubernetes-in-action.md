### 《Kubernetes in Action》

#### kubernetes API版本
- [K8S的apiVersion该用哪个](https://segmentfault.com/a/1190000017134399)
- 查看当前可用的API版本：kubectl api-versions
- v1：稳定版本，包含很多核心对象：pod、service等
- apps/v1beta2：1.8版本增加的，DaemonSet，Deployment，ReplicaSet 和 StatefulSet
- apps/v1：1.9版本增加的，包含一些通用的应用层的api组合，包含apps/v1beta2
- batch/v1：1.9版本增加的，代表job相关的api组合
- autoscaling/v1：1.8版本增加的，代表自动扩缩容的api组合

#### kubernetes 资源简称
- po：pod
- svc：service
- ing：ingress
- ns：namespaces
- rc：replicaController，类似replicaSets，已过时
- rs：replicaSets，维护和监控pod
- ds：daemonSets，一个节点一个pod
- pv：persistentVolumes，持久卷
- pvc：persistentVolumeChaim，持久卷声明
- sc：storageClass，存储类（pvc中引用了sc则根据sc动态创建pv）

#### 存活探针和就绪探针
- replicaSets 通过存活探针判断pod是否挂了，挂了就新启一个pod
- replicaSets 通过就绪探针判断一个新pod是否已经启动好了，好了就给流量
- 探针的探测机制有三种：
  1. http get
  1. tcp 连接
  1. exec 执行容器的命令

#### job 资源
- spec.completions: 4 #顺序执行4个pod
- spec.parallelism: 2 #最多并行2个pod
- template.spec.restartPolicy: OnFailure #设置为Never则失败了就不管
- PS：CronJob资源可以定时执行

#### service 资源
- service 保证了集群内/外的客户端对一组Sets的访问地址不变
- service 还可以为集群外的服务创建service，相当于服务代理
- 集群内的客户端发现 service 服务的ip和端口的方式有三种：
  1. 环境变量
  1. dns服务
  1. FQDN连接服务
- 集群外的客户端访问 service 的三种方式
  1. nodePort，启动后每个节点都开放了相同端口，缺点是如果某节点挂了，客户端不知道
  1. loadBalance，需要云服务商对应的支持
  1. Ingress，匹配不同的host和port到对应的service
- headless 服务：kind还是service，但是clusterIP是None。nslookup它的dns，返回每个pod的ip

#### 章节6，共享卷
- emptyDir：临时共享卷，删除pod，卷就没了，可以指定存储介质是内存
- hostPath：存储介质是节点的目录
- gitRepo：通过git仓库初始化卷
- nfs：nfs网络共享卷
- configMap：配置文件
- secret：私密的配置文件，可以存储tls证书、imagePullSecret
- 持久卷，通过持久卷和持久卷声明来屏蔽底层的存储技术：
  1. 持久卷：kind是persistentVolumes，spec指定存储介质，如nfs或者谷歌gce、亚马逊ebs
  1. 持久卷声明：kind是persistentVolumeChaim，spec.resources.requests申请存储
  1. pod中使用持久卷声明：kind是pod，spec.volumes.persistentVolumeChaim指定持久卷声明
- 持久卷pvc定义的访问模式accessModes：
  1. (RWO) ReadWriteOnce 可被一个节点读写挂载
  1. (ROX) ReadOnlyMany 可被多个节点只读挂载
  1. (RWX) ReadWriteMany 可被多个节点读写挂载
- 持久卷pv的ReclaimPolicy回收策略
  1. Retain (保留) 保留数据，需要管理员手动清理
  1. Recycle (回收) 清除PV中的数据，效果相当于执行删除命令
  1. Delete (删除) 与PV相连的后端存储完成volume的删除操作，常见于云服务商的存储服务
- 持久卷pv的STATUS状态
  1. Available: PV状态，表示可用状态，还未被任何PVC绑定
  1. Bound: 已绑定，已经绑定到某个PVC
  1. Released: 已释放，对应的pvc已经删除，但资源还没有被集群收回
  1. Failed: PV自动回收失败
- 持久卷存储插件分为：
  1. In-tree插件，如kubernetes.io/aws-ebs
  1. Out-of-tree Flex-volume，Kubernetes 1.2开始支持，部署复杂
  1. Out-of-tree CSI，Kubernetes 1.9开始支持，如ebs.csi.aws.com
- 持久卷，通过kubectl get csinodes获取CSI的插件安装信息
- 持久卷，各云存储的[一些限制](https://kubernetes.io/zh/docs/concepts/storage/volumes/)
- 持久卷，aws-ebs的使用：
  1. [参考资料](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
  1. 安装CSI：kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"
  1. 设置权限：secret中带iam的key_id和access_key；给实例附加IAM角色，在后台或者cli都可以操作
  1. 参考demo：https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/dynamic-provisioning
  1. 成功后在后台可以看到卷会从available状态变成in-use状态

#### 章节7，configMap和secret
1. secret命令：kubectl create secret [command] $secretName [options]，其中command有三种：docker-registry、tls、generic
1. secret创建：kubectl create secret docker-registry my-secret --docker-server=xxx --docker-username=xxx --docker-password=xxx --docker-email=xxx
1. secret查看：kubectl get secret

#### 章节8，容器内如何访问资源的元数据
1. 可用的元数据
  1. pod的名称、IP、所在的命名空间、所在的节点、所归属的服务账户
  1. 每个容器请求的cpu和内存的使用量
  1. 每个容器可以使用的cpu和内存的限制
  1. pod的标签、注解
1. /api/v1/namespaces/<namespace>/pods

#### 章节9，deployment
1. replicaController的两个问题：在滚动升级时，是靠客户端多次发指令完成的；只能删一个pod增加一个pod
1. 创建一个deployment的同时会创建一个replicaSets

#### 章节10，statefulSet
1. 不用statefulSet，每个副本pod都是共享一个存储卷（单点性能问题）。
1. statefulSet保证pod副本有固定的主机名

#### 章节11，kubernetes包含哪些组件
* [Kubernetes 组件](https://kubernetes.io/zh/docs/concepts/overview/components/)
* 控制平面：
  1. kube-apiserver：对外提供Kubernetes API
  1. kube-scheduler：调度Pod在Node上运行
  1. kube-controller-manager：运行多个控制器进程
    * 节点控制器：负责在节点出现故障时进行通知和响应
    * 任务控制器：Job相关的controller
    * 端点控制器：关联Service和Pod
    * 服务帐户和令牌控制器：为新的命名空间创建默认帐户和API访问令牌
  1. etcd：高可用一致性kv数据库
* 工作节点：
  1. kubelet：接收各类机制提供给它的PodSpecs，然后管理容器
  1. kubelet-proxy：是集群每个节点上的网络代理，维护节点上的网络规则
  1. 容器运行时：容器运行环境是负责运行容器的软件
* 插件：
  1. 网络插件
  1. DNS
  1. Dashboard

#### 章节12，api服务器认证
1. 身份认证方式：
  1. 客户端证书
  1. http header头的token
  1. http basic认证
1. 用户分为普通用户和serviceAccount（给pod的应用使用）
1. 角色分为角色（针对命名空间的资源）和ClusterRole（集群级别的资源，不是命名空间的资源）

#### 章节13，安全问题
1. 限定不用root用户运行
1. 不能写宿主机根目录
1. 网络隔离







