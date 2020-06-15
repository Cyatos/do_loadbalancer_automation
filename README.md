# Digital Ocean Load Balancer Automation

## Setup package
### Clone repository
`git clone https://github.com/Cyatos/do_loadbalancer_automation.git`
### Setup API token from Digital Token
Add environment variable DO_TOKEN=API_TOKEN
### Install the package
`pip install editable .`

## Usage Directions
### Detach Droplet from load balancer
`dolb_cli --lb_name=<loadbalancer_name> detach [<droplet_name1>, <droplet_name2]`
### Attach Droplet from load balancer
`dolb_cli --lb_name=<loadbalancer_name> attach [<droplet_name1>, <droplet_name2]`
