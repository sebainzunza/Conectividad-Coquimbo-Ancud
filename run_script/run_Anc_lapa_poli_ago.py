import sys
from datetime import datetime, timedelta
import numpy as np
import math
#import pandas as pd
#from opendrift.readers import reader_global_landmask
#from opendrift.readers import reader_netCDF_CF_generic
from opendrift.readers import reader_ROMS_native
#from opendrift.models.larvaloco import SeaLice
#from opendrift.models.oceandrift import OceanDrift
#from opendrift.models.virtual_conDVM import LarvaVirtual
from opendrift.models.virtual_sinDVM import LarvaVirtual

o = LarvaVirtual(loglevel=0)

filename = 'croco_his_hija3_M01-M12.nc';
#filecoord = 'PuntosCosta.txt';
fileshape = 'AMrocaAncud.shp'
mosa_native = reader_ROMS_native.Reader(filename)
mosa_native.interpolation='linearND'
o.add_reader(mosa_native)
print(mosa_native)  
start_date = mosa_native.start_time  + timedelta(days=309) # 5 agosto 2000
#end_date = mosa_native.end_time

outname='Part_Anc_lapa_ago_poli'
#particulas_total=10000
dias_deriva = 6 # PLD lapa
num_part = 1   # 7200 =1 per hour  for 1 month
#mindep = -20
#maxdep = -40
#zd = np.random.rand(num_part)
#zd = zd*(maxdep - mindep) + mindep
all = np.empty([0,7])
o.set_config('general:coastline_action', 'previous')
o.set_config('IBM:complete_pld',dias_deriva)
#paso = 1;
for j in range(0,6): 
    frec_seed = timedelta(days=j*5) # frecuencia : cada 5 dias por 3 meses
    for i in range(0,24):
        for c in range(1,111):
            ini_date = start_date + frec_seed + timedelta(hours=i) 
            print(ini_date)

            o.seed_from_shapefile(fileshape,
                              number = num_part, 
                              layername = None,
                              featurenum = c, 
                              time = ini_date)
                              
lons_start = o.elements_scheduled.lon
lats_start = o.elements_scheduled.lat
time_start = o.elements_scheduled_time

o.run(end_time = ini_date + timedelta(days=dias_deriva),
    time_step=timedelta(minutes=60),
    outfile = outname + '.nc',
    export_variables=['status','time'])
    #o.plot(linecolor='z', 'trayect_dia'+str(i)++'.png')

index_of_first, index_of_last = o.index_of_activation_and_deactivation()
lons = o.get_property('lon')[0]
lats = o.get_property('lat')[0]
status = o.get_property('status')[0]
tiempo = o.get_time_array()[0]

lons_end = lons[index_of_last, range(lons.shape[1])]
lats_end = lats[index_of_last, range(lons.shape[1])]
status_end = status[index_of_last, range(lons.shape[1])]
time_end   = [tiempo[i] for i in index_of_last]

uno = np.column_stack([time_start, lons_start, lats_start, time_end, lons_end, lats_end, status_end])
all = np.append(all, uno, axis=0)
        
    #paso = paso + 1
   # outname='trayect_ene_hr_'+ str(i) +'.png';
   # o.plot(linecolor='z', filename = outname)
np.savetxt('Part_Anc_lapa_ago_poli.txt', all, fmt='%s %.4f %.4f %s %.4f %.4f %i')
print(o)
#print("Guardando Figura")
#o.plot(linecolor='z', filename = outname + '.png')
#o.set_config('environment:fallback:y_sea_water_velocity', 0)
#o.animation(filename = outname + '.mp4')
print("Fin simulacion")
