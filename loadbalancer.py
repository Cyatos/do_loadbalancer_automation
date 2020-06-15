import requests as req
import os
import fire

class LoadBalancer:
    def __init__(self, lb_name):
        DO_TOKEN = os.environ.get('DO_TOKEN')
        self.headers = {"Authorization": f"Bearer {DO_TOKEN}"}
        self.base_url = f'https://api.digitalocean.com/v2/'
        self.dets = self._get_lb_details_by_name(lb_name)
        self.droplets = self._get_all_droplets()

    def _get_lb_details_by_name(self, lb_name):
        response = req.get(url=f"{self.base_url}load_balancers",
                           headers=self.headers)
        data = response.json()
        droplet_details = {}
        for lb in data['load_balancers']:
            if lb['name'] == lb_name:
                self.lb_name = lb_name
                self.lb_id = lb['id']
                for droplet_id in lb['droplet_ids']:
                    droplet_details.update(self._get_droplet_details_by_id(droplet_id))
                lb_data = {lb['name']: {'ip': lb['ip'], 'droplets': droplet_details}}
        return lb_data

    def _get_droplet_details_by_id(self, droplet_id):
        response = req.get(url=f"{self.base_url}droplets/{droplet_id}", headers=self.headers)
        data = response.json()
        return {data['droplet']['name']: {'ip_address': data['droplet']['networks']['v4'][0]['ip_address'],
                'id': droplet_id}}

    def _get_all_droplets(self):
        response = req.get(url=f"{self.base_url}droplets", headers=self.headers)
        data = response.json()
        droplets = {}
        for droplet in data['droplets']:
            droplets.update({droplet['name']: {'id': droplet['id'],
                                               'ip': droplet['networks']['v4'][0]['ip_address']}})
        return droplets

    def detach(self, droplet_names):
        url = f"{self.base_url}load_balancers/{self.lb_id}/droplets"
        droplet_list = []
        for droplet in droplet_names:
            try:
                droplet_list.append(self.dets[self.lb_name]['droplets'][droplet]['id'])
            except KeyError:
                return "Droplet not attached"
        payload = {"droplet_ids": droplet_list}
        response = req.delete(url=url, json=payload, headers=self.headers)
        if response.status_code == 204:
            return "Success"
        else:
            return "Failed"

    def attach(self, droplet_names):
        url = f"{self.base_url}load_balancers/{self.lb_id}/droplets"
        droplet_list = []
        for droplet in droplet_names:
            try:
                droplet_list.append(self.droplets[droplet]['id'])
            except KeyError:
                return "Droplet doesn't exist"
        payload = {"droplet_ids": droplet_list}
        response = req.post(url=url, json=payload, headers=self.headers)
        if response.status_code == 204:
            return "Success"
        else:
            return "Failed"


def main():
    fire.Fire(LoadBalancer)
