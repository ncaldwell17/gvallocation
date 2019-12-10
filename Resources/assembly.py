import geopandas as gpd
import numpy as np
import pandas as pd
import os

from beat_data import Beat_Data

class Assembly_Data(object):
    def assign_score(self, boolean_score):
        if boolean_score == True:
            new_boolean_score = 1
            return new_boolean_score
        if boolean_score == False:
            new_boolean_score = 0
            return new_boolean_score
    
    def __init__(self, geokey):
        self.geokey = geokey
        if self.geokey == 'beat':
            self.geoclass = Beat_Data()
        self.assembly = self.geoclass.homicides_per_beat[['beat_no', 'geometry']].copy()
        self.homs = self.geoclass.homicides_per_beat[['beat_no', 'count_homicides']].copy()
        self.shoots = self.geoclass.shootings_per_beat[['beat_no', 'count_shootings']].copy()
        self.outreach_per_beat = self.geoclass.outreach_per_beat
        self.edges = self.geoclass.edges_per_beat
        self.top25_homicides = self.geoclass.top25_homicides
        self.top25_shootings = self.geoclass.top25_shootings
        self.top10_homicides = self.geoclass.top10_homicides
        self.top10_shootings = self.geoclass.top10_shootings
        self.top5_homicides = self.geoclass.top5_homicides
        self.top5_shootings = self.geoclass.top5_shootings
        self.top1_homicides = self.geoclass.top1_homicides
        self.top1_shootings = self.geoclass.top1_shootings
        
        self.my_assemblyData = self.assembly.merge(self.homs, on='beat_no', how='left')
        self.my_assemblyData = self.my_assemblyData.merge(self.shoots, on="beat_no", how='left')
        self.my_assemblyData = self.my_assemblyData.merge(self.outreach_per_beat, on="beat_no", how="outer")
        self.my_assemblyData['num_workers'] = self.my_assemblyData['num_workers'].fillna(0)
        self.my_assemblyData = self.my_assemblyData.merge(self.edges, on="beat_no", how="left")
        
        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top25_homicides['beat_no'])
        self.my_assemblyData['in_top25_hom'] = self.pdseries

        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top25_shootings['beat_no'])
        self.my_assemblyData['in_top25_shoot'] = self.pdseries

        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top10_homicides['beat_no'])
        self.my_assemblyData['in_top10_hom'] = self.pdseries

        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top10_shootings['beat_no'])
        self.my_assemblyData['in_top10_shoot'] = self.pdseries

        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top5_homicides['beat_no'])
        self.my_assemblyData['in_top5_hom'] = self.pdseries

        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top5_shootings['beat_no'])
        self.my_assemblyData['in_top5_shoot'] = self.pdseries

        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top1_homicides['beat_no'])
        self.my_assemblyData['in_top1_hom'] = self.pdseries

        self.pdseries = self.my_assemblyData['beat_no'].eq(self.top1_shootings['beat_no'])
        self.my_assemblyData['in_top1_shoot'] = self.pdseries
        
        self.my_assemblyData['in_top25_hom'] = self.my_assemblyData['in_top25_hom'].apply(self.assign_score)
        self.my_assemblyData['in_top25_shoot'] = self.my_assemblyData['in_top25_shoot'].apply(self.assign_score)
        self.my_assemblyData['in_top10_hom'] = self.my_assemblyData['in_top10_hom'].apply(self.assign_score)
        self.my_assemblyData['in_top10_shoot'] = self.my_assemblyData['in_top10_shoot'].apply(self.assign_score)
        self.my_assemblyData['in_top5_hom'] = self.my_assemblyData['in_top5_hom'].apply(self.assign_score)
        self.my_assemblyData['in_top5_shoot'] = self.my_assemblyData['in_top5_shoot'].apply(self.assign_score)
        self.my_assemblyData['in_top1_hom'] = self.my_assemblyData['in_top1_hom'].apply(self.assign_score)
        self.my_assemblyData['in_top1_shoot'] = self.my_assemblyData['in_top1_shoot'].apply(self.assign_score)