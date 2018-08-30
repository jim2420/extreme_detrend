from mpl_toolkits.basemap import Basemap, cm, shiftgrid,interp,maskoceans
from netCDF4 import Dataset as NetCDFFile
import numpy as N
import matplotlib.pyplot as plt
import numpy.ma as ma
from statsmodels.stats.weightstats import DescrStatsW
import matplotlib.colors as colors
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
import scipy.signal

mai=NetCDFFile('mai_irr_fert.nc','r')
maiir = mai.variables['totalyield'][61:116,:,:]
mai1=NetCDFFile('mai_fert.nc','r')
mai = mai1.variables['totalyield'][61:116,:,:]
maiir= ma.masked_where(maiir<=0.0,maiir)
mai= ma.masked_where(mai<=0.0,mai)

region=NetCDFFile('/scratch2/scratchdirs/tslin2/plot/globalcrop/data/Ctry_halfdeg.nc','r')
cou = region.variables['MASK_Country'][:,:]
lonab1=region.variables['Lon'][:]
cou,lonab = shiftgrid(0.5,cou,lonab1,start=True)

region=NetCDFFile('/global/project/projectdirs/m1602/datasets4.full/arbit_init_state_05x05.nc','r')
ind = region.variables['REGION_MASK'][:,:]
lona=region.variables['lon'][:]
lata=region.variables['lat'][:]

isam1=NetCDFFile('/scratch2/scratchdirs/tslin2/plot/globalcrop/data/luh2area_850_2015_corrcrop.nc','r')
meareaisam1 = isam1.variables['fmai_tt'][1150,:,:]#2000
meareaisam1= ma.masked_where(meareaisam1<=500.0,meareaisam1)
x=55
meareaisam=N.zeros((x,360,720))
ind1=N.zeros((x,360,720))
gridarea=N.zeros((x,360,720))
cou1=N.zeros((x,360,720))
for i in range(0,x):
	ind1[i,:,:]=ind[:,:]
	meareaisam[i,:,:]=meareaisam1[:,:]
	cou1[i,:,:]=cou[:,:]
maiir= ma.masked_where(ind1!=1.0,maiir)
mai= ma.masked_where(ind1!=1.0,mai)

maiir= ma.masked_where(cou1>=11600,maiir)
mai= ma.masked_where(cou1>=11600,mai)
maiir= ma.masked_where(cou1<11500,maiir)
mai= ma.masked_where(cou1<11500,mai)

maiir= ma.masked_where(meareaisam<=500.0,maiir)
mai= ma.masked_where(meareaisam<=500.0,mai)

#maiir_avg=N.ma.average(maiir,axis=0)
#mai_avg=N.ma.average(mai,axis=0)
maiir=ma.filled(maiir, fill_value=0.)
mai=ma.filled(mai, fill_value=0.)

jj = N.array([2,3,1,0])
jg = N.array([2,3,1,0])

jjd=scipy.signal.detrend(jj)
print jj
print jjd
j1=ma.masked_where(jg<=1.0, jj)
#j1=ma.filled(j1, fill_value=0)
print j1
jjd1=scipy.signal.detrend(j1,bp=j1)
print jjd1

for i in range(0,360):
	for j in range(0,720):
	        slope[i,j], intercept[i,j], r_value, p_value, std_err = scipy.stats.linregress(gg,mai[:,i,j])
                slope_irr[i,j], intercept_irr[i,j], r_value, p_value, std_err = scipy.stats.linregress(gg,maiir[:,i,j])

print slope_irr[255,546],intercept_irr[255,546]


for i in range(0,360):
        for j in range(0,720):
		for t in range(0,55):
		#	print t,gg
			linear[t,i,j]=(gg[t]*slope[i,j])+intercept[i,j]
			linear_irr[t,i,j]=(gg[t]*slope_irr[i,j])+intercept_irr[i,j]
print linear_irr[:,255,546]
maiir_avg1,lona1 = shiftgrid(180.5,maiir_avg1,lona,start=False)
mai_avg1,lona1 = shiftgrid(180.5,mai_avg1,lona,start=False)
#print maiir_avg1

##1961 is zero
cmap = plt.cm.RdYlGn
bounds=[-50,-40,-30,-20,-10,0,10,20,30,40,50]

norm = colors.BoundaryNorm(bounds, cmap.N)

fig = plt.figure(figsize=(20,15))

ax1 = fig.add_subplot(321)
map = Basemap(llcrnrlon=-121,llcrnrlat=20,urcrnrlon=-62,urcrnrlat=51,
    projection='lcc',lat_1=32,lat_2=45,lon_0=-95)
# load the shapefile, use the name 'states'
map.readshapefile('usshape/cb_2017_us_state_5m', name='states', drawbounds=True)

lon1,lat1 = N.meshgrid(lona1,lata)
x,y = map(lon1,lat1)
j=64-61

fc,lona1 = shiftgrid(180.5,maiir_avg[j,:,:],lona,start=False)
fcl,lona1 = shiftgrid(180.5,linear_irr[j,:,:],lona,start=False)

aa=fc/fcl*100
aa[N.isnan(aa)]=0
aa[N.isinf(aa)]=0
aa= ma.masked_where(aa==0.0,aa)

map.drawcountries()


#cs1 = map.pcolormesh(x,y,aa,cmap=cmap,norm=norm)
plt.axis('off')
#cbar = map.colorbar(cs1,location='bottom',size="5%",pad="2%",ticks=bounds,extend='both')
#cbar.ax.tick_params(labelsize=14)

ax1 = fig.add_subplot(322)
map = Basemap(llcrnrlon=-121,llcrnrlat=20,urcrnrlon=-62,urcrnrlat=51,
    projection='lcc',lat_1=32,lat_2=45,lon_0=-95)
# load the shapefile, use the name 'states'
map.readshapefile('usshape/cb_2017_us_state_5m', name='states', drawbounds=True)

fc1,lona1 = shiftgrid(180.5,mai_avg[j,:,:],lona,start=False)
fcl,lona1 = shiftgrid(180.5,linear[j,:,:],lona,start=False)

bb=fc1/fcl*100
bb[N.isnan(bb)]=0
bb[N.isinf(bb)]=0

bb= ma.masked_where(bb==0.0,bb)

map.drawcountries()
cs1 = map.pcolormesh(x,y,bb,cmap=cmap,norm=norm)
plt.axis('off')
cbar = map.colorbar(cs1,location='bottom',size="5%",pad="2%",ticks=bounds,extend='both')
cbar.ax.tick_params(labelsize=14)

ax1 = fig.add_subplot(323)
map = Basemap(llcrnrlon=-121,llcrnrlat=20,urcrnrlon=-62,urcrnrlat=51,
    projection='lcc',lat_1=32,lat_2=45,lon_0=-95)
# load the shapefile, use the name 'states'
map.readshapefile('usshape/cb_2017_us_state_5m', name='states', drawbounds=True)

j=88-61

fc,lona1 = shiftgrid(180.5,maiir_avg[j,:,:],lona,start=False)
fcl,lona1 = shiftgrid(180.5,linear_irr[j,:,:],lona,start=False)

aa1=fc/fcl*100
aa1[N.isnan(aa1)]=0
aa1[N.isinf(aa1)]=0

aa1= ma.masked_where(aa1==0.0,aa1)

map.drawcountries()
#cs1 = map.pcolormesh(x,y,aa1,cmap=cmap,norm=norm)
plt.axis('off')
#cbar = map.colorbar(cs1,location='bottom',size="5%",pad="2%",ticks=bounds,extend='both')
#cbar.ax.tick_params(labelsize=14)

ax1 = fig.add_subplot(324)
map = Basemap(llcrnrlon=-121,llcrnrlat=20,urcrnrlon=-62,urcrnrlat=51,
    projection='lcc',lat_1=32,lat_2=45,lon_0=-95)
# load the shapefile, use the name 'states'
map.readshapefile('usshape/cb_2017_us_state_5m', name='states', drawbounds=True)

fc1,lona1 = shiftgrid(180.5,mai_avg[j,:,:],lona,start=False)
fcl,lona1 = shiftgrid(180.5,linear[j,:,:],lona,start=False)

bb1=fc1/fcl*100
bb1[N.isnan(bb1)]=0
bb1[N.isinf(bb1)]=0

bb1= ma.masked_where(bb1==0.0,bb1)

map.drawcountries()
cs1 = map.pcolormesh(x,y,bb1,cmap=cmap,norm=norm)
plt.axis('off')
cbar = map.colorbar(cs1,location='bottom',size="5%",pad="2%",ticks=bounds,extend='both')
cbar.ax.tick_params(labelsize=14)

ax1 = fig.add_subplot(325)
map = Basemap(llcrnrlon=-121,llcrnrlat=20,urcrnrlon=-62,urcrnrlat=51,
    projection='lcc',lat_1=32,lat_2=45,lon_0=-95)
# load the shapefile, use the name 'states'
map.readshapefile('usshape/cb_2017_us_state_5m', name='states', drawbounds=True)

j=112-61

fc2,lona1 = shiftgrid(180.5,maiir_avg[j,:,:],lona,start=False)
fcl,lona1 = shiftgrid(180.5,linear_irr[j,:,:],lona,start=False)

aa2=fc2/fcl*100
aa2[N.isnan(aa2)]=0
aa2[N.isinf(aa2)]=0

aa2= ma.masked_where(aa2==0.0,aa2)

map.drawcountries()
#cs1 = map.pcolormesh(x,y,aa2,cmap=cmap,norm=norm)
plt.axis('off')
#cbar = map.colorbar(cs1,location='bottom',size="5%",pad="2%",ticks=bounds,extend='both')
#cbar.ax.tick_params(labelsize=14)

ax1 = fig.add_subplot(326)
map = Basemap(llcrnrlon=-121,llcrnrlat=20,urcrnrlon=-62,urcrnrlat=51,
    projection='lcc',lat_1=32,lat_2=45,lon_0=-95)
# load the shapefile, use the name 'states'
map.readshapefile('usshape/cb_2017_us_state_5m', name='states', drawbounds=True)

fc12,lona1 = shiftgrid(180.5,mai_avg[j,:,:],lona,start=False)
fcl,lona1 = shiftgrid(180.5,linear[j,:,:],lona,start=False)

bb2=fc12/fcl*100
bb2[N.isnan(bb2)]=0
bb2[N.isinf(bb2)]=0

bb2= ma.masked_where(bb2==0.0,bb2)

map.drawcountries()
cs1 = map.pcolormesh(x,y,bb2,cmap=cmap,norm=norm)
plt.axis('off')
cbar = map.colorbar(cs1,location='bottom',size="5%",pad="2%",ticks=bounds,extend='both')
cbar.ax.tick_params(labelsize=14)



plt.savefig('isamdry_1961_2015denew.jpg',bbox_inches='tight')

plt.show()


