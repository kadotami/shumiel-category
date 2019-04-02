FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

ARG project_dir=/var/www/

ADD app.py /var/www/

RUN apk add --update build-base git curl openssl perl bash sudo swig gcc gfortran \
    && mkdir /usr/src/mecab/ \
    && cd /usr/src/mecab/ \
    && mkdir -p /tmp/mecab_src/ \
    && git clone https://github.com/taku910/mecab.git  /temp/mecab_src/ \
    && mv -f /temp/mecab_src/mecab/* /usr/src/mecab/ \
    &&  ./configure --enable-utf8-only \
    && make \
    && make install \
    && rm -rf /tmp/mecab_src/ \
    && git clone https://github.com/neologd/mecab-ipadic-neologd.git /usr/src/mecab-ipadic-neologd \
    && /usr/src/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y \
    && rm -rf /usr/src/mecab-ipadic-neologd \
    && mkdir -p /tmp/build \
    && cd /tmp/build/ \
    && wget http://www.netlib.org/blas/blas-3.6.0.tgz \
    && wget http://www.netlib.org/lapack/lapack-3.6.1.tgz \
    && tar xzf blas-3.6.0.tgz \
    && tar xzf lapack-3.6.1.tgz \
    && cd /tmp/build/BLAS-3.6.0/ \
    && gfortran -O3 -std=legacy -m64 -fno-second-underscore -fPIC -c *.f \
    && ar r libfblas.a *.o \
    && ranlib libfblas.a \
    && mv libfblas.a /tmp/build/. \
    && cd /tmp/build/lapack-3.6.1/ \
    && sed -e "s/frecursive/fPIC/g" -e "s/ \.\.\// /g" -e "s/^CBLASLIB/\#CBLASLIB/g" make.inc.example > make.inc \
    && make lapacklib \
    && make clean \
    && mv liblapack.a /tmp/build/. \
    && cd / \
    && export BLAS=/tmp/build/libfblas.a \
    && export LAPACK=/tmp/build/liblapack.a \
    && cd /var/www/ \
    && pip3 install --upgrade pip \
    && pip3 install Flask \
        mecab-python3 \
        Flask-Cors \
        gunicorn \
        numpy \
        gensim \
    && rm -rf /usr/src/mecab/ \
    && rm -rf /tmp/build \
    && rm -rf /var/cache/apk/*

ENTRYPOINT ["/usr/local/bin/gunicorn", "app:app"]