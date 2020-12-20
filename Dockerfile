##
## NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
##
## PLEASE DO NOT EDIT IT DIRECTLY.
##
#
#FROM alpine:3.12
#
## ensure local python is preferred over distribution python
#ENV PATH /usr/local/bin:$PATH
#
## http://bugs.python.org/issue19846
## > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
#ENV LANG C.UTF-8
#
## install ca-certificates so that HTTPS works consistently
## other runtime dependencies for Python are installed later
#RUN apk add --no-cache ca-certificates
#
#ENV GPG_KEY E3FF2839C048B25C084DEBE9B26995E310250568
#ENV PYTHON_VERSION 3.8.5
#
#RUN set -ex \
#	&& apk add --no-cache --virtual .fetch-deps \
#		gnupg \
#		tar \
#		xz \
#	\
#	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
#	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
#	&& export GNUPGHOME="$(mktemp -d)" \
#	&& gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
#	&& gpg --batch --verify python.tar.xz.asc python.tar.xz \
#	&& { command -v gpgconf > /dev/null && gpgconf --kill all || :; } \
#	&& rm -rf "$GNUPGHOME" python.tar.xz.asc \
#	&& mkdir -p /usr/src/python \
#	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
#	&& rm python.tar.xz \
#	\
#	&& apk add --no-cache --virtual .build-deps  \
#		bluez-dev \
#		bzip2-dev \
#		coreutils \
#		dpkg-dev dpkg \
#		expat-dev \
#		findutils \
#		gcc \
#		gdbm-dev \
#		libc-dev \
#		libffi-dev \
#		libnsl-dev \
#		libtirpc-dev \
#		linux-headers \
#		make \
#		ncurses-dev \
#		openssl-dev \
#		pax-utils \
#		readline-dev \
#		sqlite-dev \
#		tcl-dev \
#		tk \
#		tk-dev \
#		util-linux-dev \
#		xz-dev \
#		zlib-dev \
## add build deps before removing fetch deps in case there's overlap
#	&& apk del --no-network .fetch-deps \
#	\
#	&& cd /usr/src/python \
#	&& gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
#	&& ./configure \
#		--build="$gnuArch" \
#		--enable-loadable-sqlite-extensions \
#		--enable-optimizations \
#		--enable-option-checking=fatal \
#		--enable-shared \
#		--with-system-expat \
#		--with-system-ffi \
#		--without-ensurepip \
#	&& make -j "$(nproc)" \
## set thread stack size to 1MB so we don't segfault before we hit sys.getrecursionlimit()
## https://github.com/alpinelinux/aports/commit/2026e1259422d4e0cf92391ca2d3844356c649d0
#		EXTRA_CFLAGS="-DTHREAD_STACK_SIZE=0x100000" \
#		LDFLAGS="-Wl,--strip-all" \
#	&& make install \
#	&& rm -rf /usr/src/python \
#	\
#	&& find /usr/local -depth \
#		\( \
#			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
#			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) \) \
#			-o \( -type f -a -name 'wininst-*.exe' \) \
#		\) -exec rm -rf '{}' + \
#	\
#	&& find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec scanelf --needed --nobanner --format '%n#p' '{}' ';' \
#		| tr ',' '\n' \
#		| sort -u \
#		| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
#		| xargs -rt apk add --no-cache --virtual .python-rundeps \
#	&& apk del --no-network .build-deps \
#	\
#	&& python3 --version
#
## make some useful symlinks that are expected to exist
#RUN cd /usr/local/bin \
#	&& ln -s idle3 idle \
#	&& ln -s pydoc3 pydoc \
#	&& ln -s python3 python \
#	&& ln -s python3-config python-config
#
## if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
#ENV PYTHON_PIP_VERSION 20.2.3
## https://github.com/pypa/get-pip
#ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py
#ENV PYTHON_GET_PIP_SHA256 6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c
#
#RUN set -ex; \
#	\
#	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
#	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; \
#	\
#	python get-pip.py \
#		--disable-pip-version-check \
#		--no-cache-dir \
#		"pip==$PYTHON_PIP_VERSION" \
#	; \
#	pip --version; \
#	\
#	find /usr/local -depth \
#		\( \
#			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
#			-o \
#			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
#		\) -exec rm -rf '{}' +; \
#	rm -f get-pip.py
#
##CMD ["python3"]
## App

WORKDIR /app

COPY ./app ./app
COPY ./requirements.txt ./requirements.txt
COPY ./gunicorn.conf.py ./gunicorn.conf.py
COPY ./entrypoint.sh ./entrypoint.sh
COPY ./init_db.py ./init_db.py
COPY ./release.sh ./release.sh

RUN chmod +x ./release.sh

# for cffi and psycopg2 (build python packages)
RUN \
 apk add --no-cache libffi libffi-dev && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN apk add postgresql-client
RUN apk add curl

EXPOSE $PORT

ENTRYPOINT ["sh", "./entrypoint.sh"]
