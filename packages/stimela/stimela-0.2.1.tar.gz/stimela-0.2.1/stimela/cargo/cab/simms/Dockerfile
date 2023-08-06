FROM kernsuite/casa
RUN pip install simms pyfits numpy

RUN mkdir -p /output /input

ADD src /code
WORKDIR /code

CMD python run.py
