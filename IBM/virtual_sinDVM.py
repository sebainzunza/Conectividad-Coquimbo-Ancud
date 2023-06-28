#!/usr/bin/env python3
"""
@author: sebainzunza
"""
#
#
#
import datetime
import numpy as np
import logging; logger = logging.getLogger(__name__)
from opendrift.models.oceandrift import Lagrangian3DArray, OceanDrift
# Defining the parameters of Larva 
# Lagrangian array creates an array of size n
# where n is the number of particles 

class LarvaVirtualElement(Lagrangian3DArray):
    """Extending Lagrangian3DArray with specific properties for virtual larva
    """
    variables = Lagrangian3DArray.add_variables([
        ('n_steps', {'dtype': np.float32,
                     'units': '',
                     'default':1})])
                      

class LarvaVirtual(OceanDrift):
    """Larva Loco (Conchalepas conchalepas) life cycle model based on the OpenDrift framework.
    """
    ElementType = LarvaVirtualElement
    
    required_variables = {
        'x_sea_water_velocity': {'fallback': 0},
        'y_sea_water_velocity': {'fallback': 0},
        'x_wind': {'fallback': 0},
        'y_wind': {'fallback': 0},
#        'upward_sea_water_velocity': {'fallback': 0},
#        'ocean_vertical_diffusivity': {'fallback': 0, 'profiles': True},
#        'surface_downward_x_stress': {'fallback': 0},
#        'surface_downward_y_stress': {'fallback': 0},
#        'turbulent_kinetic_energy': {'fallback': 0},
#        'turbulent_generic_length_scale': {'fallback': 0},
#        'sea_floor_depth_below_sea_level': {'fallback': 10000},
        'land_binary_mask': {'fallback': None}}
#        'sea_water_temperature': {'fallback': 11},
#        'sea_water_salinity': {'fallback': 34}}
        
    # The depth range (in m) which profiles shall cover
    required_profiles_z_range = [0, -50]

    def __init__(self, *args, **kwargs):
        # Calling general constructor of parent class
        super(LarvaVirtual, self).__init__(*args, **kwargs)
        
        # By default, larvas do not strand towards coastline
        self.set_config('general:coastline_action', 'previous')
        
        # IBM configuration options
        self._add_config({'IBM:complete_pld':
                              {'type': 'float', 'default': 1.0,
                               'min': 1.0, 'max': 90.0, 'units': '',
                               'description': 'Days larvae in PLD',
                               'level': self.CONFIG_LEVEL_BASIC},})
        
    def update_mortality(self):
        pld = self.get_config('IBM:complete_pld')
#        dd = self.start_time
#        current_date = datetime.datetime(year=dd.year,
#                                         month=dd.month,
#                                         day=dd.day,
#                                         hour=dd.hour,
#                                         second=dd.second)
        p=1
        self.elements.n_steps+=p
#        mort = 0.12
#        mort_rate = mort * self.time_step.total_seconds()/86400
#        self.elements.otr += mort_rate
#        if self.elements.steps == pld*24:
        self.deactivate_elements(self.elements.n_steps > pld*24, reason='dead')
#        start_to_pld = self.start_time + datetime.timedelta(days=pld)
#        self.deactivate_elements(current_date > start_to_pld, reason='dead')
        
    def update(self):
        self.update_mortality()
        self.advect_ocean_current()
        self.vertical_mixing()
