FROM ubuntu:20.04
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root
RUN mkdir -p /root/src

# COPY
ADD flashurlapi.py /root
ADD src/constants.py /root/src
ADD src/api_namespace.py /root/src
ADD src/request_handler.py /root/src
ADD src/short_url.py /root/src
ADD src/shorten_service_api.py /root/src
ADD requirements.txt /root

WORKDIR /root

RUN pip3 install -r requirements.txt
#CMD ["./flashurlapi.py","--port 6773","--records records.csv"]
