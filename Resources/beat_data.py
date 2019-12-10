import geopandas as gpd
import numpy as np
import pandas as pd
import os

from beat_assembly import Beat_Assembly

class Beat_Data():
    def write_percentiles(self, domain, dataframe):
        top25 = dataframe['count_{0}'.format(domain)].quantile(.75)
        top25 = dataframe['count_{0}'.format(domain)] > top25
        top25 = dataframe[top25]
        top10 = dataframe['count_{0}'.format(domain)].quantile(.90)
        top10 = dataframe['count_{0}'.format(domain)] > top10
        top10 = dataframe[top10]
        top5 = dataframe['count_{0}'.format(domain)].quantile(.95)
        top5 = dataframe['count_{0}'.format(domain)] > top5
        top5 = dataframe[top5]
        top1 = dataframe['count_{0}'.format(domain)].quantile(.99)
        top1 = dataframe['count_{0}'.format(domain)] > top1
        top1 = dataframe[top1]
        return top25, top10, top5, top1
    
    def __init__(self):
        self.bd = Beat_Assembly()
        self.homicides_per_beat = self.bd.homicide_assembly()
        self.shootings_per_beat = self.bd.shooting_assembly()
        self.outreach_per_beat = self.bd.outreach_assembly()
        self.edges_per_beat = self.bd.edge_assembly()

        self.top25_homicides = self.write_percentiles("homicides", self.homicides_per_beat)[0]
        self.top25_homicides = self.top25_homicides.rename(columns={'count_homicides': 'count'})

        self.top25_shootings = self.write_percentiles("shootings", self.shootings_per_beat)[0]
        self.top25_shootings = self.top25_shootings.rename(columns={'count_shootings': 'count'})

        self.top10_homicides = self.write_percentiles("homicides", self.homicides_per_beat)[1]
        self.top10_homicides = self.top10_homicides.rename(columns={'count_homicides': 'count'})

        self.top10_shootings = self.write_percentiles("shootings", self.shootings_per_beat)[1]
        self.top10_shootings = self.top10_shootings.rename(columns={'count_shootings': 'count'})

        self.top5_homicides = self.write_percentiles("homicides", self.homicides_per_beat)[2]
        self.top5_homicides = self.top5_homicides.rename(columns={'count_homicides': 'count'})

        self.top5_shootings = self.write_percentiles("shootings", self.shootings_per_beat)[2]
        self.top5_shootings = self.top5_shootings.rename(columns={'count_shootings': 'count'})

        self.top1_homicides = self.write_percentiles("homicides", self.homicides_per_beat)[3]
        self.top1_homicides = self.top1_homicides.rename(columns={'count_homicides': 'count'})

        self.top1_shootings = self.write_percentiles("shootings", self.shootings_per_beat)[3]
        self.top1_shootings = self.top1_shootings.rename(columns={'count_shootings': 'count'})