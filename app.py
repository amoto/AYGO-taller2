#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from taller2.taller2_stack import Taller2Stack

app = core.App()
Taller2Stack(app,
             "Taller2Stack",
             key_name='taller2',
             vpc_id='vpc-01d7af960ab4e093d',
             sg_id='sg-0c593922f1e85cb52',
             env=core.Environment(account='154983279932', region='us-east-1'),
             )

app.synth()
