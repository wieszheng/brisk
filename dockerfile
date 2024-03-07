FROM python:3.8 as builder
WORKDIR /
COPY ./requirements.txt ./requirements.txt
RUN python -m venv /brisk/venv  \
    && /szrapi/venv/bin/pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && /szrapi/venv/bin/python -m pip install --upgrade pip \
    && /szrapi/venv/bin/python -m pip install -r requirements.txt \
    && apt update -y \
    && apt upgrade -y \
    && apt install -y tzdata \
    && apt install -y wget \


FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /innos
COPY . .
COPY --from=builder /brisk/venv/ /brisk/venv/
COPY --from=builder /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 7777
CMD ["/brisk/venv/bin/supervisord", "-c", "/brisk/supervisor.conf"]
