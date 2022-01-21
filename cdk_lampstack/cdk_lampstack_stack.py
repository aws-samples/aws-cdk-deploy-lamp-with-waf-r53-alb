'''
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 '''

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from vars import *
import os
import sys
import vars
from constructs import Construct

from aws_cdk import (
    App, Stack, Aws, CfnOutput, Tags, Fn,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    aws_wafv2 as wafv2,
    aws_certificatemanager as acm,
    aws_ec2 as ec2,
    aws_iam as iam
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.


sys.path.append(os.path.abspath(os.curdir))

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

# import WAF arn from  waf_regoinal stack
wafacl_alb_arn = Fn.import_value("WafRegionalStack:WafAclRegionalArn")


class CdkLampstackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # VPC: Create in existing VPC in a private subnet
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=var_vpc_id)

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                                          edition=ec2.AmazonLinuxEdition.STANDARD,
                                                          virtualization=ec2.AmazonLinuxVirt.HVM,
                                                          storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE)

        # Instnace Volume
        block_device_volume = autoscaling.BlockDeviceVolume.ebs(
            volume_size=8,
            encrypted=True,
        )

        block_device = autoscaling.BlockDevice(
            device_name="/dev/xvda",
            volume=block_device_volume,
        )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            "AmazonSSMManagedInstanceCore"))

        # Instance
        asg = autoscaling.AutoScalingGroup(self, "myASG", instance_type=ec2.InstanceType(var_ec2_type),
                                           machine_image=amzn_linux, vpc=vpc, role=role,
                                           vpc_subnets=ec2.SubnetSelection(
                                               subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                                           user_data=ec2.UserData.custom(
                                               user_data),
                                           block_devices=[block_device]
                                           )

        # Import existing certificate
        cert_arn = vars.cert_arn
        certificate = acm.Certificate.from_certificate_arn(
            self, 'Certificate', certificate_arn=cert_arn)

        # ALB
        alb = elbv2.ApplicationLoadBalancer(
            self, "lampALB", vpc=vpc, internet_facing=True,)

        alb.set_attribute(
            key="routing.http.drop_invalid_header_fields.enabled", value="true")

        https_listener = alb.add_listener("ALBListenerHttps", port=443, certificates=[
                                          certificate], protocol=elbv2.ApplicationProtocol.HTTPS, ssl_policy=elbv2.SslPolicy.TLS12)
        https_listener.add_targets("Target", port=80, targets=[asg])

        https_listener.connections.allow_default_port_from_any_ipv4(
            "Open to the world")

        asg.scale_on_request_count("AModestLoad", target_requests_per_minute=1)

        wafv2.CfnWebACLAssociation(self, 'WAFACLAssociateALB', resource_arn=alb.load_balancer_arn,
                                   web_acl_arn=wafacl_alb_arn)

        CfnOutput(self, "LoadBalancer", export_name="LoadBalancer",
                  value=alb.load_balancer_dns_name)
