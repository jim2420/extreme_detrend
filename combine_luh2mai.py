from mpl_toolkits.basemap import Basemap, cm, shiftgrid,interp,maskoceans
from netCDF4 import Dataset as NetCDFFile
import numpy as N
import matplotlib.pyplot as plt
import glob
import numpy.ma as ma
from scipy.interpolate import griddata
import matplotlib.colors as colors

def yieldout(year):
        bb=year-1900
	bb1=year-850
	region1=NetCDFFile('/scratch2/scratchdirs/tslin2/plot/globalcrop/data/luh2area_850_2015_corrcrop.nc','r')
	maitrop1 = region1.variables['fmai_rf'][1150,:,:]
        maitropi1=region1.variables['fmai_irr'][1150,:,:]
	maitrop1=ma.masked_where(maitrop1<=0,maitrop1)
        maitrop1=ma.filled(maitrop1, fill_value=0.)
	maitropi1=ma.masked_where(maitropi1<=0,maitropi1)
	maitropi1=ma.filled(maitropi1, fill_value=0.)
        lonisam=region1.variables['lon'][:]

        maitrop,lonisam1 = shiftgrid(180.5,maitrop1,lonisam,start=False)
        maitropi,lonisam1 = shiftgrid(180.5,maitropi1,lonisam,start=False)

	maizetor=maitrop
	maizetoi=maitropi

	maizetrop=maitrop+maitropi

	maizeto = maitrop+maitropi


        isam=NetCDFFile('mai_fert.nc','r')
        clmtropf = isam.variables['totalyield'][bb-1,:,:]

	clm2=NetCDFFile('mai_irr_fert.nc','r')
	clmtropfi = clm2.variables['totalyield'][bb-1,:,:]

        lonisam=clm2.variables['lon'][:]


        clmtropf,lonisam1 = shiftgrid(180.5,clmtropf,lonisam,start=False)
        clmtropfi,lonisam1 = shiftgrid(180.5,clmtropfi,lonisam,start=False)
        print lonisam1



	clmtropf= ma.masked_where(maitrop<=0,clmtropf)
	clmtropf=ma.filled(clmtropf, fill_value=0.)

	clmtropfi= ma.masked_where(maitropi<=0,clmtropfi)
	clmtropfi=ma.filled(clmtropfi, fill_value=0.)

        yield_clmtf=clmtropf
        yield_clmtf = ma.masked_where(yield_clmtf<=0,yield_clmtf)
        yield_clmtf=ma.filled(yield_clmtf, fill_value=0.)

        yield_clmtfi=clmtropfi
        yield_clmtfi = ma.masked_where(yield_clmtfi<=0,yield_clmtfi)
        yield_clmtfi=ma.filled(yield_clmtfi, fill_value=0.)


	area=NetCDFFile('/scratch2/scratchdirs/tslin2/plot/globalcrop/data/gridareahalf_isam.nc','r')
	gridarea = area.variables['cell_area'][:,:]
	gridlon = area.variables['lon'][:]
	gridlat=area.variables['lat'][:]
	gridarea,gridlon = shiftgrid(180.5,gridarea,gridlon,start=False)


	lon2,lat2 = N.meshgrid(gridlon,gridlat)


	map = Basemap(projection ='cyl', llcrnrlat=-65, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='c')
	x,y = map(lon2,lat2)

	yield_clmtf=maskoceans(x,y,yield_clmtf)
	yield_clmtf = ma.masked_where(maizeto<=0,yield_clmtf)

	yield_clmtfi=maskoceans(x,y,yield_clmtfi)
	yield_clmtfi = ma.masked_where(maizeto<=0,yield_clmtfi)

	clmy=((yield_clmtf*maizetor)+(yield_clmtfi*maizetoi))/((maizetoi)+(maizetor))
        areall=(maizetoi)+(maizetor)
	clmall=((yield_clmtf*maizetor)+(yield_clmtfi*maizetoi))



       
        return clmy,areall,clmall
areaa= N.zeros((115, 360, 720))
yiep= N.zeros((115, 360, 720))
yief= N.zeros((115, 360, 720))
years = range(1901, 2016)
for i, yeara in enumerate(years):


	yie=yieldout(yeara)
        yief[i, :, :] = yie[0]
        areaa[i,:,:]=yie[1]
        yiep[i,:,:]=yie[2]


area=NetCDFFile('/scratch2/scratchdirs/tslin2/plot/globalcrop/data/gridareahalf_isam.nc','r')
gridarea = area.variables['cell_area'][:,:]
gridlon = area.variables['lon'][:]
gridlat=area.variables['lat'][:]
gridarea,gridlon = shiftgrid(180.5,gridarea,gridlon,start=False)
#print gridlon
gg= N.zeros((115, 360, 720))
for i in range(0,115):
	gg[i,:,:]=gridarea[:,:]
yiey=yiep/(gg*0.0001)

ncfile=NetCDFFile('isamhiscru_mai_luh2_2000.nc','w',format='NETCDF3_64BIT_OFFSET')
ncfile.createDimension('lat', 360)
ncfile.createDimension('lon', 720)
ncfile.createDimension('time', 115)

times = ncfile.createVariable('time', 'f8', ('time',))
latitudes = ncfile.createVariable('lat', 'f8', ('lat',))
longitudes = ncfile.createVariable('lon', 'f8', ('lon',))
maize= ncfile.createVariable('yield', 'f8', ('time','lat','lon'),fill_value=-9999.)
maize1= ncfile.createVariable('area', 'f8', ('time','lat','lon'),fill_value=-9999.)
maize2= ncfile.createVariable('production', 'f8', ('time','lat','lon'),fill_value=-9999.)
maize3= ncfile.createVariable('yieldy', 'f8', ('time','lat','lon'),fill_value=-9999.)

latitudes[:] = gridlat
longitudes[:] = gridlon
times[:] = years
maize[:]=yief
maize1[:]=areaa
maize2[:]=yiep
maize3[:]=yiey

maize.units = 't/ha'
maize1.units = 'ha'
maize2.units = 'tonnes'
maize3.units = 't/ha over gridareas'



latitudes.units = 'degrees_north'
longitudes.units = 'degrees_east'

latitudes.long_name = 'latitude'
longitudes.long_name = 'longitude'


ncfile.close()





