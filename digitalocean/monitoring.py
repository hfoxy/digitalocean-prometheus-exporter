import time

from digitalocean.api import API
from digitalocean.droplets import Droplet
from prometheus_client import Gauge, Enum


labelnames = ['name', 'region', 'size']
digitalocean_droplet_cpu_usage_idle = Gauge('digitalocean_droplet_cpu_usage_idle', 'Droplet\'s CPU usage', labelnames)
digitalocean_droplet_cpu_usage_iowait = Gauge('digitalocean_droplet_cpu_usage_iowait', 'Droplet\'s CPU usage', labelnames)
digitalocean_droplet_cpu_usage_irq = Gauge('digitalocean_droplet_cpu_usage_irq', 'Droplet\'s CPU usage', labelnames)
digitalocean_droplet_cpu_usage_nice = Gauge('digitalocean_droplet_cpu_usage_nice', 'Droplet\'s CPU usage', labelnames)
digitalocean_droplet_cpu_usage_softirq = Gauge('digitalocean_droplet_cpu_usage_softirq', 'Droplet\'s CPU usage', labelnames)
digitalocean_droplet_cpu_usage_steal = Gauge('digitalocean_droplet_cpu_usage_steal', 'Droplet\'s CPU usage', labelnames)
digitalocean_droplet_cpu_usage_system = Gauge('digitalocean_droplet_cpu_usage_system', 'Droplet\'s CPU usage', labelnames)
digitalocean_droplet_cpu_usage_user = Gauge('digitalocean_droplet_cpu_usage_user', 'Droplet\'s CPU usage', labelnames)


class DropletMonitoring:

    def __init__(self, api: API, droplet: Droplet):
        self.api = api
        self.droplet = droplet

        self.id = droplet.id
        self.name = droplet.name
        self.size_slug = droplet.size_slug
        self.region_slug = droplet.region_slug

    def fetch_stats(self):
        end = time.time()
        start = end - 30
        response = self.api.get("/v2/monitoring/metrics/droplet/cpu", {'host_id': self.id, 'start': start, 'end': end})
        if response['status'] == 'success':
            data = response['data']
            for result in data['result']:
                if len(result['values']) > 0:
                    metric = None
                    if result['metric']['mode'] == 'idle':
                        metric = digitalocean_droplet_cpu_usage_idle
                    elif result['metric']['mode'] == 'iowait':
                        metric = digitalocean_droplet_cpu_usage_iowait
                    elif result['metric']['mode'] == 'irq':
                        metric = digitalocean_droplet_cpu_usage_irq
                    elif result['metric']['mode'] == 'nice':
                        metric = digitalocean_droplet_cpu_usage_nice
                    elif result['metric']['mode'] == 'softirq':
                        metric = digitalocean_droplet_cpu_usage_softirq
                    elif result['metric']['mode'] == 'steal':
                        metric = digitalocean_droplet_cpu_usage_steal
                    elif result['metric']['mode'] == 'system':
                        metric = digitalocean_droplet_cpu_usage_system
                    elif result['metric']['mode'] == 'user':
                        metric = digitalocean_droplet_cpu_usage_user

                    value = result['values'][-1]
                    metric.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(value[1])
