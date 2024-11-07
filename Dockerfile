FROM python:3.11
LABEL authors="zmzzmqa"

# 复制 requirements.txt 文件
COPY ./requirements.txt /app/requirements.txt

# 复制应用代码到容器中
COPY ./ /app

# 安装依赖
RUN apt upgrade &&\
    apt update &&\
    pip install --no-cache-dir -r requirements.txt &&\

# 设置启动命令
CMD ["python", "/app/app.py"]