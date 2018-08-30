#!/bin/sh
module load cdo

echo "writing out yield"

name=( soy_irr_fert soy_fert )

for i in {0..1}
do
 for f in {1901..2016}
  do
   echo $f ${name[i]}  
cd /scratch2/scratchdirs/tslin2/isam/maisoy_cheyenne/his_cru/new/${name[i]}/output
   echo *_crop_$f.nc crop_$f.nc
   cdo selname,total_gfna,total_gWS,n_deficit,g_drainage,g_sur_runoff *_crop_$f.nc crop_$f.nc
   cdo setyear,$f crop_$f.nc sam_$f.nc
  done
cdo mergetime sam_*.nc ${name[i]}_stress.nc
rm sam_*.nc
rm crop_*.nc
mv ${name[i]}_stress.nc /scratch2/scratchdirs/tslin2/isam/extreme
done

name=( mai_irr_fert )

for i in {0..0}
do
 for f in {1901..2016}
  do
   echo $f ${name[i]}  
   cd /scratch2/scratchdirs/tslin2/isam/maisoy_cheyenne/his_cru/fixedirr/${name[i]}/output
   echo *_crop_$f.nc crop_$f.nc
   cdo selname,total_gfna,total_gWS,n_deficit,g_drainage,g_sur_runoff *_crop_$f.nc crop_$f.nc
   cdo setyear,$f crop_$f.nc sam_$f.nc
  done
cdo mergetime sam_*.nc ${name[i]}_stress.nc
rm sam_*.nc
rm crop_*.nc
mv ${name[i]}_stress.nc /scratch2/scratchdirs/tslin2/isam/extreme
done
 

name=( mai_fert )

for i in {0..0}
do
 for f in {1901..2016}
  do
   echo $f ${name[i]}  
   cd /scratch2/scratchdirs/tslin2/isam/maisoy_cheyenne/his_cru/${name[i]}/output
   echo *_crop_$f.nc crop_$f.nc
   cdo selname,total_gfna,total_gWS,n_deficit,g_drainage,g_sur_runoff *_crop_$f.nc crop_$f.nc
   cdo setyear,$f crop_$f.nc sam_$f.nc
  done
cdo mergetime sam_*.nc ${name[i]}_stress.nc
rm sam_*.nc
rm crop_*.nc
mv ${name[i]}_stress.nc /scratch2/scratchdirs/tslin2/isam/extreme
done

