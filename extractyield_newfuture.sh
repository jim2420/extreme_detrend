#!/bin/sh
module load cdo

echo "writing out yield"

name=( soy_irr_fert mai_irr_fert  mai_fert soy_fert)

for i in {1..1}
do
 for f in {2015..2100}
  do
   echo $f ${name[i]}  
cd /scratch2/scratchdirs/tslin2/isam/maisoy_cheyenne/rcp45new/${name[i]}/output
   echo *_crop_$f.nc crop_$f.nc
   cdo selname,totalyield *_crop_$f.nc crop_$f.nc
   cdo setyear,$f crop_$f.nc sam_$f.nc
  done
cdo mergetime sam_*.nc ${name[i]}.nc
rm sam_*.nc
rm crop_*.nc
done
 
