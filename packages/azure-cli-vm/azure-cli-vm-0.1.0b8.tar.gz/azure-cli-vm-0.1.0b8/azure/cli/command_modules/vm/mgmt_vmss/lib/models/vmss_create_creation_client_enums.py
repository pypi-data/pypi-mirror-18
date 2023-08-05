#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------
#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from enum import Enum


class authenticationType(Enum):

    password = "password"
    ssh = "ssh"


class customOsDiskType(Enum):

    windows = "windows"
    linux = "linux"


class dnsNameType(Enum):

    none = "none"
    new = "new"


class loadBalancerType(Enum):

    new = "new"
    existing = "existing"
    none = "none"


class osDiskType(Enum):

    provided = "provided"
    custom = "custom"


class osType(Enum):

    win2012_r2_datacenter = "Win2012R2Datacenter"
    win2012_datacenter = "Win2012Datacenter"
    win2008_r2_sp1 = "Win2008R2SP1"
    custom = "Custom"


class overprovision(Enum):

    true = "true"
    false = "false"
    true = "True"
    false = "False"


class publicIpAddressAllocation(Enum):

    dynamic = "dynamic"
    static = "static"


class publicIpAddressType(Enum):

    none = "none"
    new = "new"
    existing_name = "existingName"


class storageCaching(Enum):

    read_only = "ReadOnly"
    read_write = "ReadWrite"


class upgradePolicyMode(Enum):

    manual = "manual"
    automatic = "automatic"


class virtualNetworkType(Enum):

    new = "new"
    existing = "existing"


class DeploymentMode(Enum):

    incremental = "Incremental"
    complete = "Complete"
