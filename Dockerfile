FROM atlassian/bamboo-agent-base
USER root
RUN apt-get update && \
    apt-get install maven -y && \
    apt-get install git -y

USER ${BAMBOO_USER}
RUN ${BAMBOO_USER_HOME}/bamboo-update-capability.sh "system.builder.mvn3.Maven 3.3" /usr/share/maven
RUN ${BAMBOO_USER_HOME}/bamboo-update-capability.sh "system.git.executable" /usr/bin/git
