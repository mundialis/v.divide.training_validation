FROM mundialis/grass-py3-pdal:latest-alpine

WORKDIR /src
COPY . /src
COPY .github/workflows/test.sh /src
RUN apk add gcc make
RUN test -e requirements.txt && pip3 install -r requirements.txt || echo "No requirements.txt"

# RUN grass --tmp-location XY --exec g.extension g.download.location
# RUN grass --tmp-location XY --exec \
#     g.download.location url=https://grass.osgeo.org/sampledata/north_carolina/nc_spm_full_v2alpha2.tar.gz path=/grassdb

RUN grass -c epsg:3358 /grassdb/nc_spm_empty --exec bash test.sh
