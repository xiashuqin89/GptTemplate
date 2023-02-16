FROM python:3.6.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

ENTRYPOINT ["streamlit", "run", "form.py", "--server.port=8080", "--server.address=0.0.0.0"]