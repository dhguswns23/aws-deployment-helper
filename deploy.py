from base import AWS_CLI, FlowLine
from settings import AWS_CONFIG, DEFAULT_NAME, AS_SUFFIX, \
    SUFFIX, LOG_FILE
from utils import read_json, write_json, tprint, tprint_end, tprint_error

iam = AWS_CONFIG['IAM']
ec2 = AWS_CONFIG['EC2']
tg = AWS_CONFIG['TARGET_GROUP']
asg = AWS_CONFIG['AUTO_SCALING_GROUP']
sec_group = AWS_CONFIG["SECURITY_GROUP"]
vpc = AWS_CONFIG["VPC"]

aws = AWS_CLI(iam['ACCESS_KEY'], iam['SECRET_KEY'])

name = "{0}-{1}".format(DEFAULT_NAME, SUFFIX)
as_name = "{0}{1}-{2}".format(DEFAULT_NAME, AS_SUFFIX, SUFFIX)

log_format = {
    "AUTOSCALING_GROUP": {
        "NAME": as_name,
    }
}

msg = "Creating AMI from {}".format(ec2['PROD_ID'])
ami = tprint(msg, aws.create_ec2_image, ec2["PROD_ID"], name)
ami_id = ami['ImageId']

msg = "Creating Launch Configuration from {}".format(ami_id)
launch_config = tprint(msg, aws.create_launch_configuration, ami_id, name, sec_group)

msg = "Creating Auto Scaling from {}".format(name)
auto_scaling = tprint(msg, aws.create_auto_scaling_group, as_name, name, asg["MIN"], asg["MAX"], vpc["SUBNET"])

msg = "Attaching Auto Scaling group to {}".format(name)
auto_scaling = tprint(msg, aws.attach_load_balancer_target_groups, as_name, tg["ARN"])
try:
    log = read_json(LOG_FILE)
    msg = "Deleting previous Auto Scaling group '{}'".format(as_name)
    tprint(msg, aws.delete_auto_scaling_group, log["AUTOSCALING_GROUP"]["NAME"], True)
except Exception as e:
    print(e)
    tprint_error("Absence of log file causes ignoring deletion process.")
    
msg = "Wrapping Up log files..."
tprint_end(msg)
write_json(LOG_FILE, log_format)
