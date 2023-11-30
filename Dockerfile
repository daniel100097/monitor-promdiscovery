FROM python:3.6


WORKDIR /app


RUN adduser --disabled-password --gecos '' --uid 1000 app \
   && mkdir /app -p && chown -R 1000:1000 /app

USER 1000

COPY --chown=1000:1000 requirements.txt  . 

RUN pip install -r requirements.txt 


COPY --chown=1000:1000 .  . 

RUN python setup.py sdist && \
        pip install dist/*

COPY ./entrypoint.sh /entrypoint.sh

CMD ["/entrypoint.sh"]