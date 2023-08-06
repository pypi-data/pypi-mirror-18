#!/bin/bash

source ../bootstrap.sh

set_sdk_link 'https://developer.nordicsemi.com/nRF5_SDK/nRF5_SDK_v11.x.x/nRF5_SDK_11.0.0_89a8197.zip'

set_dl_location ../tmp

set_patch_file 'sdk110_connectivity.patch'

run
