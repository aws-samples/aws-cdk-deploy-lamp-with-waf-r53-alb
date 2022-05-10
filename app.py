#!/usr/bin/env python3
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

import os
from vars import *
from aws_cdk import App, Environment

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.


from cdk_lampstack.cdk_lampstack_stack import CdkLampstackStack
from cdk_lampstack.waf_regional import WafRegionalStack

# env = {'region': 'us-east-1'}
app = App()
env_USA = Environment(account=var_account_id, region=var_region)
waf_description = "Deploy WAF ACL"
lamp_description = "Deploy LAMP Stack (qs-1t1gmgopk)"

waf = WafRegionalStack(app, "WafRegionalStack",
                       env=env_USA, description=waf_description)
lamp = CdkLampstackStack(app, "CdkLampstackStack",
                         env=env_USA, description=lamp_description)
lamp.add_dependency(waf)
app.synth()
