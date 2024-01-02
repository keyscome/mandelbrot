from diagrams import Diagram, Cluster

from diagrams.onprem.database import MySQL
from diagrams.onprem.monitoring import Prometheus

from diagrams.aws.compute import EC2
from diagrams.onprem.container import Docker

from diagrams.onprem.queue import Kafka


with Diagram("Observation"):
    
    with Cluster("IM"):
        im_api = EC2("API")
        im_media = EC2("Meida")
        im_db = MySQL("IM-Web")
    
    media_indicator_queue = Kafka("Media Indicator")
    
    with Cluster("devops"):
        prom = Prometheus("Metric TSDB")
        with Cluster("Observation"):
            ob_db = MySQL("Observation")
            ob_api = Docker("API")
            ob_front = Docker("Frontend")
            ob_mic = Docker("Indicator-Comsumer")
    
    im_api << prom
    im_media >> media_indicator_queue >> ob_mic >> prom
    
    im_db - im_media
    im_db - im_api
    
    im_db >> ob_api
    ob_db - ob_api
    prom >> ob_api
    
    im_api - ob_front
    ob_api - ob_front
    