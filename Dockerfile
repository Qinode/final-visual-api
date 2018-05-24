FROM python:3.6

WORKDIR /api
ADD . /api

RUN pip install -r requirements.txt
RUN chmod a+x /api/src/run.sh
EXPOSE 8081
CMD ["/api/src/run.sh"]
