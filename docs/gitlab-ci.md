### gitlab-ci配置

#### docker下安装runner
1. [gitlab+gitlab-runner实现自动打包docker镜像](https://lx1990.github.io/2018/07/31/gitlab+gitlab-runner%E5%AE%9E%E7%8E%B0%E8%87%AA%E5%8A%A8%E6%89%93%E5%8C%85docker%E9%95%9C%E5%83%8F/)

```
#第一步，启动一个runner容器
docker run -d --name gitlab-runner --restart always \
     -v /srv/gitlab-runner/config:/etc/gitlab-runner \
     -v /var/run/docker.sock:/var/run/docker.sock \
     gitlab/gitlab-runner:latest

#第二步，配置关联gitlab，executor=docker，image=docker:18
docker exec -it gitlab-runner gitlab-runner register

#第三步，vim /srv/gitlab-runner/config/config.toml，修改 privileged = true
```

#### 配置.gitlab-ci.yml
```
image: docker:18

variables:
  DOCKER_HOST: tcp://docker:2375/
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

services:
  - docker:18-dind
 
before_script:
  - echo xxx | docker login -u xxx registry.cn-qingdao.aliyuncs.com --password-stdin
  
build:
  stage: build
  script:
    - hostname
    - pwd
    - docker build -t registry.cn-qingdao.aliyuncs.com/qinhan/simida:image-php-fpm70 .
    - docker push registry.cn-qingdao.aliyuncs.com/qinhan/simida:image-php-fpm70
```