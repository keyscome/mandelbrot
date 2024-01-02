from diagrams import Diagram, Cluster

from diagrams.onprem.database import MySQL
from diagrams.onprem.monitoring import Prometheus

from diagrams.aws.compute import EC2
from diagrams.onprem.container import Docker

from diagrams.onprem.queue import Kafka

from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Users

from diagrams.generic.device import Mobile
from diagrams.generic.device import Tablet
from diagrams.generic.os import Windows
from diagrams.generic.os import LinuxGeneral

from diagrams.programming.language import Go
from diagrams.programming.language import Python
from diagrams.programming.framework import React
from diagrams.programming.framework import Vue


with Diagram("Observation"):
    
    
    with Cluster("IM"):
        im_api = EC2("API")
        im_media = EC2("Meida")
        im_webapp = EC2("Webapp")
        im_front = Vue("Frontend")
        
    with Cluster("DB"):
        im_db = MySQL("IM")
        ob_db = MySQL("Observation")
    
    media_indicator_queue = Kafka("Media Indicator")
    
    with Cluster("Observation"):
        prom = Prometheus("Metric TSDB")
        with Cluster("APP"):
            ob_front = React("Frontend")
            ob_metric_api = Go("metric-API")
            ob_mic = Go("Indicator-Comsumer")
            with Cluster("statistics"):
                ob_statistics_job = Python("job")
                ob_statistics_api = Go("API")
    
    nginx = Nginx("Nginx")
    users = Users("Users")
    with Cluster("Clients"):
        clients = [
            Windows("Windows"),
            LinuxGeneral("Linux"),
            Mobile("Mobile"),
            Tablet("Tablet"),
        ]
    
    im_media - im_api
    im_media - im_webapp
    im_api - im_front
    im_webapp - im_front
    im_api << prom
    im_webapp << prom
    im_media >> media_indicator_queue >> ob_mic >> prom
    
    im_db - im_media
    im_db - im_api
    
    im_db >> ob_statistics_job
    prom - ob_statistics_api
    ob_statistics_job - ob_statistics_api
    ob_db - ob_statistics_api
    
    im_api - ob_front
    ob_statistics_api - ob_front
    
    nginx - im_webapp
    nginx - im_front
    nginx - ob_front
    
    clients >> ob_metric_api
    ob_metric_api >> prom
    nginx - clients
    clients - users
    