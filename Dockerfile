FROM python:3.10
RUN mkdir -p automatic
WORKDIR /automatic
COPY pip.conf /root/.pip/pip.conf
COPY requirements.txt /automatic
RUN pip install -r /automatic/requirements.txt
RUN rm -rf /automatic
COPY . /automatic
CMD [ "python", "./main.py"]