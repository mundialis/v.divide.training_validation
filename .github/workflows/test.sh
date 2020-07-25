#!/usr/bin/env bash

# Author: Vaclav Petras (wenzeslaus)
# commit: https://github.com/OSGeo/grass-addons/commit/3d73a400926c0d1af67dc28f58fbf22007ca8cb4

# fail on non-zero return code from a subprocess
set -e

grass --tmp-location XY --exec \
    g.extension g.download.location
grass --tmp-location XY --exec \
    g.download.location url=http://fatra.cnr.ncsu.edu/data/nc_spm_full_v2alpha2.tar.gz dbase=$HOME

grass --tmp-location XY --exec \
    python3 -m grass.gunittest.main \
        --grassdata $HOME --location nc_spm_full_v2alpha2 --location-type nc \
        --min-success 30
