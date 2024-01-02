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


with Diagram("Observation"):
    
    
    with Cluster("IM"):
        im_api = EC2("API")
        im_media = EC2("Meida")
        im_webapp = EC2("Webapp")
        im_front = EC2("Frontend")
        
    with Cluster("DB"):
        im_db = MySQL("IM")
        ob_db = MySQL("Observation")
    
    media_indicator_queue = Kafka("Media Indicator")
    
    with Cluster("Observation"):
        prom = Prometheus("Metric TSDB")
        with Cluster("APP"):
            ob_statistics_api = Docker("statistics-API")
            ob_metric_api = Docker("metric-API")
            ob_front = Docker("Frontend")
            ob_mic = Docker("Indicator-Comsumer")
    
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
    
    im_db >> ob_statistics_api
    ob_db - ob_statistics_api
    prom - ob_statistics_api
    
    im_api - ob_front
    ob_statistics_api - ob_front
    
    nginx - im_webapp
    nginx - im_front
    nginx - ob_front
    
    clients >> ob_metric_api
    ob_metric_api >> prom
    nginx - clients
    clients - users
    