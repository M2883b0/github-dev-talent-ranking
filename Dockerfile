FROM python:3.11:latest
LABEL authors="zmzzmqa"

# 设置工作目录
WORKDIR /app

# 复制应用代码到容器中
COPY . /app

# 安装依赖
RUN apt upgrade &&\
    apt update &&\
    pip install --no-cache-dir -r requirements.txt &&\


# 设置启动命令
CMD ["python", "start"]