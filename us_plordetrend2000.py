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
maiir = mai.variables['totalyield'][99:112,:,:]
mai1=NetCDFFile('mai_fert.nc','r')
mai = mai1.variables['totalyield'][99:112,:,:]
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
x=13
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

maiir=ma.filled(maiir, fill_value=0.)
mai=ma.filled(mai, fill_value=0.)

maiir_avg=scipy.signal.detrend(maiir,axis=0)
mai_avg=scipy.signal.detrend(mai,axis=0)
print maiir[:,255,546]
print maiir_avg[:,255,546]
maiir_avg1=N.median(maiir_avg,axis=0)
mai_avg1=N.median(mai_avg,axis=0)
slope=N.zeros((360,720))
intercept=N.zeros((360,720))
gg=N.zeros(13)
gg=N.arange(1,14)
linear=N.zeros((x,360,720))
linear_irr=N.zeros((x,360,720))
slope_irr=N.zeros((360,720))
intercept_irr=N.zeros((360,720))
maiir_avg1,lona1 = shiftgrid(180.5,maiir_avg1,lona,start=False)

for i in range(0,360):
	for j in range(0,720):
	        slope[i,j], intercept[i,j], r_value, p_value, std_err = scipy.stats.linregress(gg,mai[:,i,j])
                slope_irr[i,j], intercept_irr[i,j], r_value, p_value, std_err = scipy.stats.linregress(gg,maiir[:,i,j])

print slope_irr[255,546],intercept_irr[255,546]


for i in range(0,360):
        for j in range(0,720):
		for t in range(0,x):
		#	print t,gg
			linear[t,i,j]=(gg[t]*slope[i,j])+intercept[i,j]
			linear_irr[t,i,j]=(gg[t]*slope_irr[i,j])+intercept_irr[i,j]
print linear_irr[:,255,546]

cmap = plt.cm.RdYlGn
bounds=[-50,-40,-30,-20,-10,0,10,20,30,40,50]
#bounds=[-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5]

norm = colors.BoundaryNorm(bounds, cmap.N)

fig = plt.figure(figsize=(10,10))

ax1 = fig.add_subplot(121)
map = Basemap(llcrnrlon=-121,llcrnrlat=20,urcrnrlon=-62,urcrnrlat=51,
    projection='lcc',lat_1=32,lat_2=45,lon_0=-95)
# load the shapefile, use the name 'states'
map.readshapefile('usshape/cb_2017_us_state_5m', name='states', drawbounds=True)

lon1,lat1 = N.meshgrid(lona1,lata)
x,y = map(lon1,lat1)
j=111-99

fc,lona1 = shiftgrid(180.5,maiir_avg[j,:,:],lona,start=False)
fcl,lona1 = shiftgrid(180.5,linear_irr[j,:,:],lona,start=False)

aa=fc/fcl*100
aa[N.isnan(aa)]=0
aa[N.isinf(aa)]=0
aa= ma.masked_where(aa==0.0,aa)

map.drawcountries()


cs1 = map.pcolormesh(x,y,aa,cmap=cmap,norm=norm)
plt.axis('off')
cbar = map.colorbar(cs1,location='bottom',size="5%",pad="2%",ticks=bounds,extend='both')
cbar.ax.tick_params(labelsize=14)

ax1 = fig.add_subplot(122)
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


plt.savefig('isamdry_2000_2012ano.jpg',bbox_inches='tight')

plt.show()


