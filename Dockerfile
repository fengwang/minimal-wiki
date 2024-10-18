FROM python:alpine3.8
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt && \
pip install https://github.com/fengwang/markdown/archive/master.zip --upgrade
EXPOSE 8895
ENTRYPOINT ["python"]
CMD ["wiki.py"]

