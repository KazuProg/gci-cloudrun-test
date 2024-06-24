FROM python:slim

ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1

# locales-allだと420.29MBだが、これだと211.52MBになる
RUN apt-get update && \
	apt-get install -y locales && \
	sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen && \
	locale-gen

WORKDIR /app

COPY src/ /app/

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "main.py"]
