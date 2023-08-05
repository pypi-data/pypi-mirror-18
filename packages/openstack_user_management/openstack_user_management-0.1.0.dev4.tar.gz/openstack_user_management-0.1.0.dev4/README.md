Usage
=====

You may use this library with the register panel patch that we forked from openstack/horizon  
  
$ git clone https://github.com/b3lab/openstack_user_management.git  
$ cd openstack_user_management/dist  
$ sudo pip install openstack_user_management-<version>.tar.gz  
  
Make sure you have the clouds.yaml file including the credentials to connect to your OpenStack platform  
inside /etc/openstack directory.  
  
Example clouds.yaml
===================
```  
clouds:  
  cloud-admin:  
    auth:  
      auth_url: http://<controller_hostname>:5000/v3  
      password: <password>  
      project_domain_name: default  
      project_name: admin  
      user_domain_name: default  
      username: admin  
    domain_name: Default  
    identity_api_version: '3'  
    region_name: RegionOne  
```
If you do not use cloud-admin name, you should change this value in  
openstack_user_management.connectors.openstack_connector  
  
  
Setup Development Environment
=============================
  
Clone repository  
$ git clone https://github.com/b3lab/openstack_user_management.git  
$ cd openstack_user_management  
  
Create a virtual environment  
$ virtualenv ./.venv  
  
Switch to virtual environment  
$ source ./.venv/bin/activate  
  
Install requirements  
$ pip install -r requirements.txt  
  
Install unittest requirements  
$ pip install -r test-requirements.txt  
