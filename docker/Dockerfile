FROM alpine:3.17.3

ARG build_date=unspecified

LABEL org.opencontainers.image.title="Auto-vSDA" \
      org.opencontainers.image.description="Automated vSDA" \
      org.opencontainers.image.created="${build_date}"

RUN apk add --no-cache gcc musl-dev make

RUN apk add --no-cache python3
RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

RUN apk add --no-cache openssh

RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools wheel

RUN apk --update add git sshpass libffi-dev libxml2-dev libxslt-dev python3-dev openssl-dev openssh-keygen libssh-dev

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN ansible-galaxy collection install community.general
RUN ansible-galaxy collection install community.vmware
RUN ansible-galaxy collection install cisco.dnac
RUN ansible-galaxy collection install cisco.ise

ARG terraform_version=1.4.6

RUN apk --update add wget unzip cdrkit curl
RUN wget --quiet https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip
RUN unzip terraform_${terraform_version}_linux_amd64.zip
RUN mv terraform /usr/bin
RUN rm terraform_${terraform_version}_linux_amd64.zip


ENV PYTHONDONTWRITEBYTECODE=1
ENV ANSIBLE_HOST_KEY_CHECKING=false
ENV ANSIBLE_RETRY_FILES_ENABLED=false
ENV ANSIBLE_SSH_PIPELINING=true
ENV ANSIBLE_LOCAL_TMP=/tmp
ENV ANSIBLE_REMOTE_TMP=/tmp

WORKDIR /ansible