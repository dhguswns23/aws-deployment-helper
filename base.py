import boto3
import sys, json

class AWS_CLI(object):
    DEFAULT_REGION = 'ap-northeast-2'
    def __init__(self, ACCESS_KEY, SECRET_KEY, region=None):
        self.ACCESS_KEY = ACCESS_KEY
        self.SECRET_KEY = SECRET_KEY
        self.format = 'json'

        if region == None:
            self.region = AWS_CLI.DEFAULT_REGION
        else:
            self.region = region

    def get_ec2(self):
        return boto3.client('ec2',
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY)

    def get_auto_scaling(self):
        return boto3.client('autoscaling',
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY)

    def create_ec2_image(self, instance_id, name, no_reboot=True):
        ec2 = self.get_ec2()
        return ec2.create_image(InstanceId=instance_id, Name=name, NoReboot=no_reboot)

    def create_launch_configuration(self, ami, name, security_group, instance_type=None):
        if instance_type == None:
            instance_type = 't2.micro'
        autoscaling = self.get_auto_scaling()
        return autoscaling.create_launch_configuration(
            LaunchConfigurationName=name,
            ImageId=ami,
            InstanceType=instance_type,
            SecurityGroups=security_group)

    def create_auto_scaling_group(self, name, configuration, min_size, max_size, vpc_zone):
        autoscaling = self.get_auto_scaling()
        return autoscaling.create_auto_scaling_group(
            AutoScalingGroupName=name,
            LaunchConfigurationName=configuration,
            MaxSize=max_size,
            MinSize=min_size,
            VPCZoneIdentifier=vpc_zone)

    def attach_load_balancer_target_groups(self, asg_name, tg_name):
        autoscaling = self.get_auto_scaling()
        return autoscaling.attach_load_balancer_target_groups(
            AutoScalingGroupName=asg_name,
            TargetGroupARNs=tg_name
        )

    def attach_load_balancers(self, as_name, lb_name):
        autoscaling = self.get_auto_scaling()
        return autoscaling.attach_load_balancers(
            AutoScalingGroupName=as_name,
            LoadBalancerNames=lb_name)

    def delete_auto_scaling_group(self, name, force_delete=False):
        autoscaling = self.get_auto_scaling()
        return autoscaling.delete_auto_scaling_group(
            AutoScalingGroupName=name,
            ForceDelete=force_delete
        )

class Edge(object):
    def __init__(self, meta, func, *args, **kwargs):
        self.meta = meta
        self.func = func
        self.args = args
        self.kwargs = kwargs


class FlowLine(object):
    def __init__(self):
        self.queue = []

    def add_queue(self, meta, func, *args, **kwargs):
        edge = Edge(meta, func, *args, **kwargs)
        self.queue.append(edge)

    def add_queue_as_edge(self, edge):
        self.queue.append(edge)

    def run(self):
        for edge in self.queue:
            print(edge.meta.get('message'))
            args = edge.args
            kwargs = edge.kwargs
            edge.func(*args, **kwargs)



