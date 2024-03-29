### docker相关

#### docker基础
1. 配置远程2375端口管理，vim /etc/default/docker，加上DOCKER_OPTS="-H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock"
1. 更换镜像源，/etc/docker/daemon.json，加上{"registry-mirrors": ["http://hub-mirror.c.163.com"]}
1. 启动redis：docker run --network subnet01 --name container-redis -p 6379:6379 -d redis --restart=always
1. 容器开机启动：docker update --restart=always container-redis

#### 配置DNS
1. [配置dns - docker](https://yeasy.gitbook.io/docker_practice/network/dns)
1. vim /etc/docker/daemon.json，加上{"dns": ["114.114.114.114"]}
1. 查看生效没有：docker run -it --rm busybox cat /etc/resolv.conf

#### docker 跨主机网络：overlay 简介
1. [再说docker及云中的网络连接](https://ying-zhang.github.io/cloud/2016/vm-net-2/)，介绍了overlay的历史
1. [“深入浅出”来解读Docker网络核心原理](https://blog.51cto.com/ganbing/2087598)，讲了沙盒、端点、overlay驱动
1. [docker 跨主机网络：overlay 简介](https://cizixs.com/2016/06/13/docker-overlay-network/)，overlay需要swarm master节点，运行swarm manager服务

#### docker network的ipvlan模式、macvlan模式
1. [Macvlan 和 IPvlan](https://www.cnblogs.com/menkeyi/p/11374023.html)，ipvlan l2和macvlan类似，ipvlan l3有点像路由器
1. [Macvlan与ipvlan](https://xiazemin.github.io/MyBlog/docker/2019/07/11/ipvlan.html)，介绍了一些大厂的网络方案

#### docker容器访问宿主机服务（或者其他容器）
1. [docker容器访问宿主机服务](https://blog.csdn.net/qq_38403662/article/details/102555888)
1. [Docker容器间利用bridge网桥实现双向通信](https://www.cnblogs.com/zouzou-busy/p/12148825.html)
1. [docker四大网络模式](https://lgzblog.com/2020/04/23/docker%E5%9B%9B%E5%A4%A7%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%BC%8F/)
1. none模式：没有网卡
1. host模式：--network host，使用宿主机网络作为容器网络
1. container模式：
  * 使用link参数和指定的容器共享IP、端口范围，当然文件系统、进程列表等还是隔离的
  * 写host，Dockerfile 添加：ip -4 route list match 0/0 | awk '{print $3 "host.docker.internal"}' >> /etc/hosts
1. bridge模式：在同一网桥的容器处于同一个局域网

```
# bridge模式
docker network ls
docker network create --subnet=172.18.0.1/24 subnet01
docker run --name=container-nginx1 --network subnet01 -d image-nginx1
docker run --name=container-nginx2 --network subnet01 -d image-nginx2

docker network create -d bridge my_bridge
docker network connect my_bridge container-db
docker network connect my_bridge container-nginx
```

#### volume 和 bind-mount
1. [跟我一起学Docker——Volume](https://www.binss.me/blog/learn-docker-with-me-about-volume/)
1. 数据卷（volume）与捆绑挂载（bind-mount）两个方式都可以与外部共享数据
1. 数据卷（volume）定义方式：
  1. Dockerfile 中指定 VOLUME /container/dir，其他容器要共享就--volumes-from container-name
  1. docker run -v /host/dir:/container/dir
1. 捆绑挂载（bind-mount）定义方式：--mount type=bind,source=/host/target,target=/container/dir
1. 捆绑挂载如果容器的那个目录非空，则内容被屏蔽，只显示宿主机的目录

#### Dockerfile命令
1. ENTRYPOINT 和 CMD
  1. CMD ["command","param1","param2"]，如果没有ENTRYPOINT，就以CMD为默认命令
  1. CMD ["param1","param2"]，传递参数给ENTRYPOINT
  1. CMD command param1 param2，以shell的方式（/bin/sh -c）执行，ENTRYPOINT这样用也是一样
1. COPY 和 ADD，ADD 多了一个功能，如果是src是url可以下载它
1. WORKDIR 和 CD：CD 只对当前行命令有效，WORKDIR 则是整体改变目录
1. ARG 和 ENV：ARG 在镜像编译时起作用，ENV 在镜像编译、运行时都起作用，其实就是环境变量
1. EXPOSE 仅仅是声明容器打算使用什么端口而已，并不会自动在宿主进行端口映射，不声明也可

#### 容器内安装telnet等
```
# 方案1：
apk add busybox-extras

# 方案2
echo 'deb http://mirrors.aliyun.com/debian/ buster main non-free contrib' > /etc/apt/sources.list \
&& echo 'deb http://mirrors.aliyun.com/debian-security buster/updates main' >> /etc/apt/sources.list \
&& echo 'deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib' >> /etc/apt/sources.list \
&& echo 'deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib' >> /etc/apt/sources.list \
&& apt-get update \
&& apt-get install telnet
```

#### docker 网络偶尔不稳定的问题
1. [docker下php程序报错php_network_getaddresses: getaddrinfo failed](https://learnku.com/laravel/t/49314)
1. 最终解决办法是配置docker的dns为114.114.114.114