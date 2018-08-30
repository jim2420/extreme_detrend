#!/bin/sh
module load cdo

echo "writing out yield"

name=(nomaizeflood)

for i in {0..0}
do
 for f in {1901..2016}
  do
   echo $f ${name[i]}  
cd /scratch2/scratchdirs/tslin2/isam/extreme/noextremeflood/output
#   echo *_crop_$f.nc crop_$f.nc
   cdo selname,denitrification,nuptake,leaching,annual_ndemand,nsupply,net_min *.bgc-yearly-2d_$f.nc crop_$f.nc
   cdo setyear,$f crop_$f.nc sam_$f.nc
  done
cdo mergetime sam_*.nc ${name[i]}_n.nc
rm sam_*.nc
rm crop_*.nc
mv ${name[i]}_n.nc /scratch2/scratchdirs/tslin2/isam/extreme
done
