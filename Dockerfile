FROM python:3.6

WORKDIR /api
ADD . /api

RUN pip install -r requirements.txt
RUN chmod a+x /api/run.sh
EXPOSE 8081
CMD ["/api/run.sh"]
