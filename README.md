# Launch Checker
JX3 service launch checker .

## Install Dependency
```bash
pip install -r ./requirements.txt
```

## Quick Start
```bash
python launch_checker.py
```

## Build A Docker Image
```bash
docker build . -t launch_checker
```


## Deploy
# 删除cms容器
docker container stop jx3box-spider;
docker container rm jx3box-spider;
docker pull registry.cn-hangzhou.aliyuncs.com/jx3box/jx3box-spider:latest;
docker container run -dt --name jx3box-spider -p 11003:11003 --restart=always --network cms registry.cn-hangzhou.aliyuncs.com/jx3box/jx3box-spider:latest;