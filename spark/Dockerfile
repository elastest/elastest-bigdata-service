FROM ubuntu:14.04


MAINTAINER s.gioldasis@gmail.com


####installing [software-properties-common] so that we can use [apt-add-repository] to install Java8
RUN apt-get update -y && apt-get install software-properties-common -y \
&&  apt-add-repository ppa:webupd8team/java -y \
&&  apt-get update -y \

####automatically agreeing on oracle license agreement [for installing java]
&&  echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections \
&&  echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections \

####installing java and supervisor
&&  apt-get install -y oracle-java8-installer \
# &&  apt-get install -y oracle-java8-set-default \
    supervisor
ENV JAVA_HOME     /usr/lib/jvm/java-8-oracle

#### Hadoop 
ENV HADOOP_LVERSION      2.7.3
ENV HADOOP_HOME         /usr/local/hadoop
ENV HADOOP_OPTS         -Djava.library.path=/usr/local/hadoop/lib/native
# RUN apt-get update && \
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget libzip2 libsnappy1 libssl-dev && \
RUN apt-get install -y libzip2 libsnappy1 libssl-dev && \
    wget http://archive.apache.org/dist/hadoop/core/hadoop-$HADOOP_LVERSION/hadoop-$HADOOP_LVERSION.tar.gz && \
    # apt-get remove -y wget && \
    # rm -rf /var/lib/apt/lists/* && \
    tar -zxf /hadoop-$HADOOP_LVERSION.tar.gz && \
    rm /hadoop-$HADOOP_LVERSION.tar.gz && \
    mv hadoop-$HADOOP_LVERSION /usr/local/hadoop && \
    mkdir -p /usr/local/hadoop/logs
ENV PATH          $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin


#### Environmental Variables
ENV SPARK_VERSION       2.1.1
ENV HADOOP_VERSION      2.7
ENV ALLUXIO_VERSION     1.5.0

#### Alluxio
ENV ALLUXIO_HOME         /opt/alluxio
RUN cd / \
	&& wget http://alluxio.org/downloads/files/${ALLUXIO_VERSION}/alluxio-${ALLUXIO_VERSION}-hadoop-${HADOOP_VERSION}-bin.tar.gz \
	&& tar xvfz alluxio-${ALLUXIO_VERSION}-hadoop-${HADOOP_VERSION}-bin.tar.gz \
	&& rm alluxio-${ALLUXIO_VERSION}-hadoop-${HADOOP_VERSION}-bin.tar.gz \
	&& mv alluxio-${ALLUXIO_VERSION}-hadoop-${HADOOP_VERSION} $ALLUXIO_HOME
ENV PATH          $PATH:$ALLUXIO_HOME/bin

#### Spark 
ENV SPARK_HOME         /opt/spark
RUN cd / \
	&& wget https://d3kbcqa49mib13.cloudfront.net/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
	&& tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
	&& rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
	&& mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME
ENV PATH          $PATH:$SPARK_HOME/bin

#####adding conf files [to be used by supervisord for running spark master/slave]
COPY master.conf /opt/conf/master.conf
COPY slave.conf /opt/conf/slave.conf



#######exposing port 8080 for spark master UI
EXPOSE 8080

#default command: running an interactive spark shell in the local mode
CMD ["/opt/spark/bin/spark-shell", "--master", "local[*]"]
