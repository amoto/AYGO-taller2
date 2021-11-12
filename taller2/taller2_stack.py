from aws_cdk import (
    core as cdk,
    aws_ec2 as ec2,
    aws_iam as iam,
)


class Taller2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, key_name: str, vpc_id: str, sg_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = self.get_role()
        vpc = self.get_vpc(vpc_id)
        sg = self.get_security_group(sg_id)

        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            'ssh',
        )
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(8090),
            '8090',
        )
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            'http',
        )

        for i in range(3):
            ec2.Instance(self,
                         "Instance_" + str(i),
                         vpc=vpc,
                         instance_type=self.get_instance_type(),
                         machine_image=self.get_machine_image(),
                         role=role,
                         init=self.get_init_configs(),
                         init_options=self.get_init_options(),
                         key_name=key_name,
                         security_group=sg,
                         )

    def get_vpc(self, vpc_id):
        vpc = ec2.Vpc.from_lookup(self, vpc_id, vpc_id=vpc_id)
        return vpc

    def get_security_group(self, sg_id):
        sg = ec2.SecurityGroup.from_security_group_id(self, sg_id, sg_id)
        return sg

    def get_instance_type(self):
        # print('get instance type')
        return ec2.InstanceType("t2.micro")

    def get_machine_image(self):
        return ec2.MachineImage.latest_amazon_linux()

    def get_role(self):
        return iam.Role.from_role_arn(
            self,
            'EMR_EC2_DefaultRole',
            'arn:aws:iam::' + cdk.Stack.of(self).account + ':role/EMR_EC2_DefaultRole'
        )

    def get_init_configs(self):
        return ec2.CloudFormationInit.from_config_sets(
            config_sets={
                # Applies the configs below in this order
                "default": [
                    "init",
                    "docker",
                    "webapp",
                ]
            },
            configs={
                "init": ec2.InitConfig([
                    ec2.InitPackage.yum("git"),
                ]),
                "docker": ec2.InitConfig([
                    ec2.InitPackage.yum("docker"),
                    ec2.InitCommand.shell_command(
                        "service docker start"),
                    ec2.InitCommand.shell_command(
                        "usermod -a -G docker ec2-user"),
                    ec2.InitCommand.shell_command(
                        "curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname "
                        "-s)-$(uname -m) -o /usr/bin/docker-compose"),
                    ec2.InitCommand.shell_command(
                        "chmod +x /usr/bin/docker-compose"),
                ]),
                "webapp": ec2.InitConfig([
                    ec2.InitCommand.shell_command("git clone https://github.com/amoto/AYGO-taller1"),
                    ec2.InitCommand.shell_command("cd AYGO-taller1 && docker-compose up -d 2> docker-compose.error"),
                ])
            }
        )

    def get_init_options(self):
        return ec2.ApplyCloudFormationInitOptions(
            config_sets=["default"],
            print_log=True,
        )
