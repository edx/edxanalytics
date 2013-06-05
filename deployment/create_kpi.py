#!/usr/bin/python
import os
import sys
import time

from boto.ec2.connection import EC2Connection

conn = EC2Connection()

def create_clean_ubuntu_instance():
    # Pop up a baseline Ubuntu image in all 'kpi' security groups
    image = conn.get_all_images(image_ids=['ami-0cdf4965'])[0] 
    security_groups = [k for k in conn.get_all_security_groups() if 'kpi' in str(k)]
    reservation = image.run(instance_type='m1.small', security_groups=security_groups, key_name = 'dev')

    # Wait for instance to appear
    while reservation.instances[0].state == 'pending':
        print ".",
        time.sleep(0.2)
        reservation.instances[0].update()

    # Tag instance
    instance.add_tag("Name", "kpi-auto")
    instance = reservation.instances[0]
    print "New instance", instance.dns_name
    return instance

def prepare_machine(machine_name):
    scpcmd = "scp -r -i ~/.aws/dev.pem {dir}/ ubuntu@{machine_name}:~/"
    os.system(scpcmd.format(machine_name = machine_name, dir="skeleton"))
    os.system(scpcmd.format(machine_name = machine_name, dir="secure"))
    
prepare_machine(os.environ['MACHINE_IP'])
