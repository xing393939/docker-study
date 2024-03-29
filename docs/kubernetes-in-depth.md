### 《Kubernetes 深入剖析》

#### 第2章 容器技术基础
* 进程隔离：利用Namespace：PID、Mount、IPC、Network、User、UTS(自定义hostname)
* 资源限制：利用Cgroups：CPU、内存、块设备I/O、带宽
* 文件系统：利用rootfs
* 分层镜像：利用UnionFS
* 如何进入到已运行的容器内：
  * 进程B利用setns共享容器A的Network Namespace
  * PS：这也是容器间共享Namespace的方法
* 如何把宿主机的目录mount到容器内：
  * 准备好rootfs后，在执行chroot之前，把目录mount到容器目录

#### 第3章 Kubernetes设计与架构
* Kubernetes的设计本质是具有普遍意义的、声明式API驱动的编排思想和最佳实践
* API编排对象：
  * Pod：容器间共享Network Namespace
  * Job：只运行一次
  * CronJob：定期运行
  * ConfigMap：配置文件
  * Secret：配置文件(私密的)
* API服务对象：
  * Service：为Pod提供固定的代理入口
  * Ingress：为Service提供公开服务
  * Horizontal-Pod-Autoscaler：基于Pod可以自动水平扩展
* 抽象基础设施：计算、存储、网络
* 抽象编排关系：亲密关系、访问关系、代理关系

#### 第4章 Kubernetes集群搭建与配置
* 声明式API
  * 不管是create还是update都是kubectl apply
  * 面向终态的分布式系统设计原则

#### 第5章 Kubernetes编排原理
* 为什么需要Pod
  * Pod内的容器可以共享Linux Namespace
  * 如果使用docker -net=容器A --volumes-from=容器A，则容器A必须先启动，使用Pod则不需要
* Pod是怎么被创建出来的
  * 先创建Infra空容器，再通过Join Network Namespace创建用户容器
* Pod级别和Container级别
  * Pod级别：和Node相关的配置，和Linux Namespace相关的属性
  * Container级别：镜像相关、生命周期Hooks
* Projected Volumes：
  * Secret：数据存放在etcd，数据更新后，Volume的内容自动更新
  * ConfigMap：数据存放在etcd，数据更新后，Volume的内容自动更新
  * DownloadApi：映射Pod的metadata成Volume，如Pod的名称、ip、容器的cpu limit、Node的ip
  * ServiceAccountToken：映射Service account的token成Volume
* 健康检查探针：
  * exec：执行自定义command，成功返回0，失败返回非0
  * httpGet：http检查
  * tcpSocket：tcp检查
* PodPreset：Pod预设置模板，先apply这个，接下来生成的Pod会继承它的属性
* Service的网络模式：
  * 使用VIP技术
  * 使用DNS技术，分两种：
    * 访问某域名，指向Service的VIP地址
    * 访问某域名，直接指向Pod的ip地址
* Toleration调度器的两个例子：
  * 集群的master Node默认有Taint=node-role.kubernetes.io/master禁止运行用户的Pod，除非指定Pod的Toleration则可以
  * 集群的Node默认有Taint=node.kubernetes.io/network-unavailable禁止没有网络的节点运行Pod，所以安装网络插件的Pod需要指定Toleration
  * PS：查看Node的Taints：kubectl get nodes -o json | jq '.items[].spec.taints'
* 控制器：
  * 控制器的源码都在github.com/kubernetes/kubernetes/tree/master/pkg/controller下
  * 它们都遵循控制循环思想：始终努力达到最终配置定义的状态
  * Deployment：每一次的更新都会生成一个新的ReplicaSet，dep控制rs的版本，rs控制pod的副本数
  * StatefulSet的网络：生成的Pod副本的name始终不变，即对应的DNS域名不变。创建从Pod-0到Pod-N(必须等到正常运行后才能创建下一个)，删除从Pod-N到Pod-0
  * StatefulSet的存储：Volume使用PVC，PVC对应的实现是PV（可能是阿里或者aws的ebs）
  * DaemonSet：每个Node只运行一个Pod。它和StatefulSet一样利用ControllerRevision进行对Pod的版本管理
  * Job和CronJob：restartPolicy=Never表示Job失败直接创建新的，=OnFailure表示重启Pod
    * Job：spec.parallelism是并行Pod的个数，spec.completions是总的所需Pod数
    * CronJob：spec.concurrencyPolicy，Allow是Job可以并行，Forbid是Job会跳过，Replace表示Job会被replace
* RBAC：
  * 三个API对象的组合：Role、RoleBinding、User(可以是Client credentials，或者来自外部认证服务)
  * 常用API对象的组合：Role、RoleBinding、ServiceAccount(它对应的用户组的name是system:serviceaccounts:{当前Namespace})
  * 查询subject.name=default的用户拥有的角色：kubectl get clusterrolebinding -o jsonpath='{range .items\[?(@.subjects\[0].name=="default")]}\[{.roleRef}]{end}'
  * PS：如果要作用于所有Namespace，则使用ClusterRole、ClusterRoleBinging
  * PS：系统内置的ClusterRole：cluster-admin、admin、edit、view

#### 第5章11~13节 声明式API和CRD
* 声明式API：apply vs create && replace，replace每次都是替换，而apply每次都是merge(可以多次修改且没有冲突)
* Istio在每个Pod里注入一个Envoy容器(高性能网络代理)：部署一个envoy-initializer控制器，检查Pod并注入Envoy容器
* CRD，自定义API对象network的例子：github.com/xing393939/samplecrd-code
  * Informer通过APIServer的LIST API获取network对象，通过WATCH API监听network对象的变化，并加入队列
  * 控制器每秒循环取队列，处理对象的变化
  * PS：也可以通过此方法对默认的API对象(如Deployment)进行二次开发
  * PS：在Kubernetes中，本地缓存一般称为Store，索引一般称为Index
  * PS：Informer使用Reflector包，它是“通过ListAndWatch机制获取并监听API对象变化”的客户端封装

#### 第5章15节 Operator工作原理
* etcd operator：会创建一个etcdCluster的CRD，etcdCluster可修改size和version
* etcd backup operator：会创建一个etcdBackup的CRD，每创建一个etcdBackup对象即备份一次
* etcd restore operator：会创建一个etcdRestore的CRD，每创建一个etcdRestore对象即备份一次
* 创建了service如何查询它的内网DNS记录？(需安装coredns等插件)
  * nslookup -q=srv {service名称}
  * PS：headless服务，是StatefulSet的pod有域名podName.serviceName.default.svc.cluster.local，否则是podIP.serviceName.default.svc.cluster.local
  * PS：headless服务，非StatefulSet的pod可以指定spec.hostname和spec.subdomain(必须等于serviceName)得到域名hostname.subdomain.default.svc.cluster.local
* ClusterIP类型的Service用于无状态的服务；Headless Service用于有状态的服务

#### 第6章 Kubernetes存储原理
* 用户创建pod，Kubernetes发现这个pod声明使用了PVC，就帮它找一个PV配对。
* 没有现成的PV，就去找对应的StorageClass，帮它新创建一个PV，然后和PVC完成绑定。
* 通过两阶段处理把PV变成Pod可用的Volume：
  * 第一阶段(Attach)：可用参数是nodeName，由运行在master节点上的AttachDetachController负责，把网络盘挂载在对应的Node
  * 第一阶段(Mount)：可用参数是dir，由每个节点上kubelet组件的内部负责，把磁盘mount到指定Pod的Volume

#### 第7章 Kubernetes网络原理
* 单机容器网络，假设docker有docker0网桥，有容器1和容器2
  * docker0网桥是充当两层交换机的角色
  * 容器被创建出来后，会创建两个虚拟网卡(Veth Peer)，一个在容器中，一个插在docker0网桥上
  * 容器1借助docker0网桥即可容器2通讯
  * 容器1借助docker0网桥——宿主机即可和其他宿主机通讯
* CNI网络插件
  * kubernetes中的CNI网桥是为了替代docker的docker0网桥的
* 跨宿主机的容器间通讯，CoreOS的Flannel项目有3个方案
  * UDP模式：容器1——docker0——flannel0设备——flanneld(8025端口)——宿主机1(eth0)
    * flannel0收到IP包后发给flanneld，flanneld在etcd找到子网对应的宿主机2的ip
    * flanneld把IP包封装成UDP包发给宿主机2的8025端口，即flanneld进程
    * 需要经过3次用户态-内核态的数据复制
  * VXLAN模式：容器1——docker0——flannel.1(VTEP设备)——宿主机1(eth0)
    * [七张图带你搞懂 Kubernetes Flannel 高性能网络插件的两种常用工作模式](https://os.51cto.com/art/202112/693234.htm)
    * 每个宿主机启动并加入flannel网络后，会在所有宿主机上记录路由规则和ARP记录
    * flannel.1收到Ip包后会进行两次封装，最后组成UDP发给宿主机2
    * 如何知道宿主机2的mac地址？通过ARP表
    * 如何知道宿主机2的ip地址？通过FDB(forwarding database)表
    * 主机的route表、ARP表、FDB表由flanneld来维护
    * 为什么用UDP包？因为这是在数据链路层，上层的TCP会保证数据的完整性
    * 性能损失在20%~30%
  * host-gw模式：容器1——cni0——宿主机1(eth0)
    * 每一个宿主机都会设置下一跳规则(借助etcd和flanneld)，即宿主机充当“网关”角色
    * 要求宿主机之间必须是两层连通的(在同一个子网)
    * 性能损失在10%左右
* 跨宿主机的容器间通讯，calico项目
  * 和Flannel项目的host-gw模式类似
  * 不同于flannel借助etcd和flanneld来维护路由信息，它借助linux内核的BGP协议
  * 要求宿主机之间必须是两层连通的(在同一个子网)
  * 若步数两层联通的，则启动IPIP模式，性能和Flannel的VXLAN模式相当
* 跨宿主机的容器间通讯，总结：
  * 主要有两种方案：
    * 隧道模式：Flannel项目的UDP模式和VXLAN模式。通过配置下一条主机的路由规则来实现互通
    * 三层网络：Flannel项目的host-gw模式和calico项目。通过在IP包外再封装一层MAC包头来实现
  * 隧道模式的优缺点：
    * 优点：简单，原因是大部分工作都是由Linux内核的模块实现了
    * 缺点：性能低
  * 三层网络的优缺点：
    * 优点：少了封包和解包的过程，性能高
    * 缺点：需要自己想办法维护路由规则；宿主机之间最好是两层连通
* 内部如何访问kubernetes集群的service：
  * 建立了my-service，就有了my-service.default.svc.cluster.local
  * spec.type=ExternalName：相当于my-service.default.svc.cluster.local被替换为my.database.example.com
  * spec.ExternalIPs：访问此ip也等于是访问my-service.default.svc.cluster.local
* 外界如何访问kubernetes集群的service：
  1. spec.type=NodePort：访问任何一台宿主机的IP均可
  1. spec.type=LoadBalancer：适合公有云，自动创建LB，并把Pod的IP配置给LB
  1. Ingress：只需要一个LB接上Ingress，配置规则转发到不同的service上。Nginx、HAProxy、Envoy、Traefik都有对应的Ingress Controller

#### 第8章 资源管理和资源调度
* Pod的spec.containers.0.resources：limits表示最高配置，requests是最低配置
* 当Eviction发生时，删除Pod的顺序
  * 首先是BestEffort类型：没有设置requests和limits
  * 其次是BurstAble类别：不满足Guaranteed条件，但至少有一个Container设置了requests
  * 最后是Guaranteed类别：同时设置requests和limits，并且requests和limit值相等
* 默认调度器kube-scheduler的预选调度策略：
  1. GeneralPredicates：检查节点的CPU和内存资源
  1. Volume相关：如EBS不能同时被两个Pod使用
  1. 宿主机相关：如Node的污点机制
  1. Pod相关：亲密性和反亲密
* 默认调度器kube-scheduler的优先策略：
  * 给符合预选规则的节点打分，范围是0~10分
* 设置Pod的优先级：
  * 先定义一个优先级：kind=PriorityClass
  * 设置Pod的spec.priorityClassName
  * 高优先级的Pod会优先调度

#### 第9章 容器运行时
* kubelet的核心是一个控制循环，驱动控制循环的四种事件：
  1. Pod更新事件
  1. Pod生命周期变化
  1. kubelet本身的执行周期
  1. 定时清理
* 支持CRI的容器：
  1. docker
  1. rkt：背靠CoreOS，已经不活跃
  1. Kata：前身是runV，背靠Intel，虚拟化轻量级的虚拟机
  1. gVisor：背靠Google，实现用户态运行的独立内核(依赖宿主机的内核)

#### 第10章 监控和日志
* Prometheus已经全面接管了kubernetes项目的整套监控体系
* 容器日志收集方案1：Node级别，以DaemonSet部署logging-agent，发送到日志后端
  * 缺点是要求应用容器的日志都输出到stdout和stderr
* 容器日志收集方案2：若应用容器的日志是写文件，塞一个sidebar容器收集它再输出到stdout和stderr
  * 作为第一种方案的补充
* 容器日志收集方案3：塞一个sidebar容器直接把日志发送到日志后端
  * 缺点是消耗资源；无法通过kubectl logs查看日志
* 容器日志收集方案4：应用容器直接把日志发给日志后端

#### 第11章 kubernetes应用管理进阶
* kubernetes的出现让企业级的PAAS不再是大公司的专利，小公司也能做
* kubernetes的定位是平台的平台，它是面向运维工程师的，不是面向业务工程师的
* OAM，Open Application Model
  * 此规范与平台无关，既可以基于kubernetes，也可以基于云平台
  * KubeVela是此规范的完整实现
  
#### 第12章 kubernetes开源社区
* 谷歌为了保持中立，成立CNCF基金来运营kubernetes
* kubernetes社区项目治理还是比较贴近谷歌风格的
* kubernetes社区最大的优点就是清楚的区分了搞政治和搞技术的人，如果这两类人大量重合就是灾难了
