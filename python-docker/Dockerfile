#Copyright (C) Chris Park 2018-2019
#Copyright (C) Allen (Jian Feng) Xie 2019
#stocksight is released under the Apache 2.0 license. See
#LICENSE for the full license text.
FROM ubuntu:20.10

LABEL maintainer="Allen (Jian Feng) Xie"

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y python3 python3-pip git curl
RUN rm -rf /var/lib/apt/lists/*

# Ensure that we can build packages from source
RUN pip3 install --upgrade pip setuptools wheel

ADD requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN [ "python3", "-c", "import nltk; nltk.download('punkt')" ]

ENTRYPOINT ["sh","startup.sh"]