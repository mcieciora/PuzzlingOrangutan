FROM jenkins/jenkins:alpine
MAINTAINER mcieciora

USER root

# Install plugins and setup jenkins instance with CASC
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# Install docker
RUN apk add --update docker openrc docker-cli-compose
RUN rc-update add docker boot