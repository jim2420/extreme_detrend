#!/bin/sh
module load cdo
module load nco
echo "writing out yield"

name=(mai_fert )
for i in {0..0}
do
cd /scratch2/scratchdirs/tslin2/isam/maisoy_cheyenne/his_cru/${name[i]}/output
rm crop_*.nc
rm crop1_*.nc
rm crop2_*.nc
 for f in {1901..2016}
  do
   echo $f ${name[i]}  
#   echo *.bgc-yearly-2d_$f.nc crop_$f.nc
   ncks -v g_Precip  *_crop_$f.nc crop_$f.nc
   ncap2 -s 'defdim("time",1);time[time]='$f';time@long_name="Time"' -O crop_$f.nc crop1_$f.nc
#   ncks -O --mk_rec_dmn time crop1_$f.nc crop2_$f.nc
   ncecat crop1_$f.nc crop2_$f.nc

# Concatenate files
   done
files=`ls crop2_*.nc`

echo $files
ncrcat -O crop2_*.nc ${name[i]}_pp.nc
rm sam_*.nc
rm crop_*.nc
rm crop1_*.nc
rm crop2_*.nc
mv ${name[i]}_pp.nc /scratch2/scratchdirs/tslin2/isam/extreme
done


name=(mai_irr_fert )
for i in {0..0}
do
cd /scratch2/scratchdirs/tslin2/isam/maisoy_cheyenne/his_cru/fixedirr/${name[i]}/output
rm crop_*.nc
rm crop1_*.nc
rm crop2_*.nc
 for f in {1901..2016}
  do
   echo $f ${name[i]}  
#   echo *.bgc-yearly-2d_$f.nc crop_$f.nc
   ncks -v g_Precip  *_crop_$f.nc crop_$f.nc
   ncap2 -s 'defdim("time",1);time[time]='$f';time@long_name="Time"' -O crop_$f.nc crop1_$f.nc
#   ncks -O --mk_rec_dmn time crop1_$f.nc crop2_$f.nc
   ncecat crop1_$f.nc crop2_$f.nc

# Concatenate files
   done
files=`ls crop2_*.nc`

echo $files
ncrcat -O crop2_*.nc ${name[i]}_pp.nc
rm sam_*.nc
rm crop_*.nc
rm crop1_*.nc
rm crop2_*.nc
mv ${name[i]}_pp.nc /scratch2/scratchdirs/tslin2/isam/extreme
done



name=(soy_irr_fert soy_fert)
for i in {0..1}
do
cd /scratch2/scratchdirs/tslin2/isam/maisoy_cheyenne/his_cru/new/${name[i]}/output
rm crop_*.nc
rm crop1_*.nc
rm crop2_*.nc
 for f in {1901..2016}
  do
   echo $f ${name[i]}  
#   echo *.bgc-yearly-2d_$f.nc crop_$f.nc
   ncks -v g_Precip  *_crop_$f.nc crop_$f.nc
   ncap2 -s 'defdim("time",1);time[time]='$f';time@long_name="Time"' -O crop_$f.nc crop1_$f.nc
#   ncks -O --mk_rec_dmn time crop1_$f.nc crop2_$f.nc
   ncecat crop1_$f.nc crop2_$f.nc

# Concatenate files
   done
files=`ls crop2_*.nc`

echo $files
ncrcat -O crop2_*.nc ${name[i]}_pp.nc
rm sam_*.nc
rm crop_*.nc
rm crop1_*.nc
rm crop2_*.nc
mv ${name[i]}_pp.nc /scratch2/scratchdirs/tslin2/isam/extreme
done





