from prometheus_client import Gauge, Enum


labelnames = ['name', 'region', 'size']
digitalocean_droplet_cpus = Gauge('digitalocean_droplet_cpus', 'Droplet\'s number of CPUs', labelnames)
digitalocean_droplet_disk_gb = Gauge('digitalocean_droplet_disk_gb', 'Droplet\'s disk size in GiB', labelnames)
digitalocean_droplet_disk_bytes = Gauge('digitalocean_droplet_disk_bytes', 'Droplet\'s disk size in bytes', labelnames)
digitalocean_droplet_memory_gb = Gauge('digitalocean_droplet_memory_gb', 'Droplet\'s total memory in GiB', labelnames)
digitalocean_droplet_memory_bytes = Gauge('digitalocean_droplet_memory_bytes', 'Droplet\'s total memory in bytes', labelnames)
digitalocean_droplet_price_hourly = Gauge('digitalocean_droplet_price_hourly', 'Droplet\'s hourly price', labelnames)
digitalocean_droplet_price_monthly = Gauge('digitalocean_droplet_price_monthly', 'Droplet\'s monthly price', labelnames)
digitalocean_droplet_running = Enum('digitalocean_droplet_running', 'Droplet\'s running status', states=['on', 'off'], labelnames=labelnames)
digitalocean_droplet_status = Enum('digitalocean_droplet_status', 'Droplet\'s status', states=['new', 'active', 'off', 'archive'], labelnames=labelnames)


class Droplets:

    def __init__(self, droplet_list):
        print(type(droplet_list))
        print(droplet_list)
        self.raw_list = droplet_list
        self.droplet_list = []
        for droplet_data in droplet_list:
            self.droplet_list.append(Droplet(droplet_data))


class Droplet:

    def __init__(self, droplet_data):
        print(droplet_data)
        self.id = droplet_data['id']
        self.name = droplet_data['name']
        self.vcpus = droplet_data['vcpus']
        self.memory_gb = droplet_data['memory']
        self.memory_bytes = self.memory_gb * 1024 * 1024 * 1024
        self.disk_gb = droplet_data['disk']
        self.disk_bytes = self.disk_gb * 1024 * 1024 * 1024
        self.locked = droplet_data['locked']
        self.size_slug = droplet_data['size']['slug']
        self.size_price_hourly = droplet_data['size']['price_hourly']
        self.size_price_monthly = droplet_data['size']['price_monthly']
        self.addresses_v4 = [data['ip_address'] for data in droplet_data['networks']['v4']]
        self.addresses_v6 = [data['ip_address'] for data in droplet_data['networks']['v6']]
        self.region_slug = droplet_data['region']['slug']
        self.region_name = droplet_data['region']['name']
        self.status = droplet_data['status']
        self.running = 'on' if self.status in ['new', 'active'] else 'off'

    def populate_metrics(self):
        digitalocean_droplet_cpus.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(self.vcpus)
        digitalocean_droplet_disk_gb.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(self.disk_gb)
        digitalocean_droplet_disk_bytes.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(self.disk_bytes)
        digitalocean_droplet_memory_gb.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(self.memory_gb)
        digitalocean_droplet_memory_bytes.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(self.memory_bytes)
        digitalocean_droplet_price_hourly.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(self.size_price_hourly)
        digitalocean_droplet_price_monthly.labels(name=self.name, region=self.region_slug, size=self.size_slug).set(self.size_price_monthly)
        digitalocean_droplet_running.labels(name=self.name, region=self.region_slug, size=self.size_slug).state(self.running)
        digitalocean_droplet_status.labels(name=self.name, region=self.region_slug, size=self.size_slug).state(self.status)
