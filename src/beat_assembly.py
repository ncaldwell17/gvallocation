import geopandas as gpd
import numpy as np
import pandas as pd
import os

class Beat_Assembly():

    def __init__(self):
        # Data Sources
        self.beat_list = np.arange(1, 278)
        d = {'beat_no': self.beat_list}
        self.assembly = pd.DataFrame(data=d)

        self.homicide_data = pd.read_csv('Data/CPD/Sep_01_2019_homicide_victims.csv')
        self.shooting_data = pd.read_csv('Data/CPD/Sep_01_2019_shooting_victims_details.csv')
        self.outreach_data = pd.read_csv('Data/Staffing/staff.csv')
        self.census_data = gpd.read_file('Data/Census/Beats/agg_aw_areal_Beats.geojson')
        self.edge_data = pd.read_csv('Data/edges.csv')

        self.beat_master = gpd.read_file('Data/Geo/Beats/geo_export_79ad3484-6fe3-40c7-bfae-0247adca4e23.shp')
        # creates a column called 'beat_no' in beat_master that gets beat_list as its series' values
        self.beat_master['beat_no'] = self.beat_list 

        # columns = ['Community', 'beat_no']
        # self.df_beats = pd.DataFrame(columns=columns)

    def homicide_assembly(self):
        # gets rid of excess data before I perform joins
        beat_filter = self.beat_master[['beat_no', 'beat_num', 'geometry']].copy()
        my_homicideData = self.homicide_data[['HOMICIDE_NO', 'BEAT_CD']].copy()
        # allows the same key to be present in both dataframes
        my_homicideData = my_homicideData.rename(columns={"BEAT_CD":"beat_num"})
        # replaces all the NaN's with 0's to avoid an error when I set the type
        my_homicideData = my_homicideData.fillna(0)
        # sets both the keys to the same datatype before I join them 
        beat_filter["beat_num"] = beat_filter["beat_num"].astype(int) 
        my_homicideData["beat_num"] = my_homicideData["beat_num"].astype(int)
        # left joins can work either way...I think. 
        hom_per_beat = beat_filter.merge(my_homicideData, on='beat_num', how='left')
        # groups unique values of homicide_IDs by their beat, but accidentally removes the geometries. 
        hom_per_beat = hom_per_beat.groupby(by='beat_no', as_index=False).agg({'HOMICIDE_NO': pd.Series.nunique})
        # creates a just beat-to-geometry dataset from the base
        beat_geos = self.beat_master[['beat_no', 'geometry']].copy()
        # rejoins the homicides by their geometries 
        # needed to merge beat_geos to hom_per_beat because the result wasn't a geopandas
        hom_per_beat = beat_geos.merge(hom_per_beat, on='beat_no', how='left')
        # renamed column to make distinction easier
        hom_per_beat = hom_per_beat.rename(columns={'HOMICIDE_NO':'count_homicides'})
        return hom_per_beat 
    
    def shooting_assembly(self):
        # gets rid of excess data before I perform joins
        beat_filter = self.beat_master[['beat_no', 'beat_num', 'geometry']].copy()
        # gets rid of excess data before I join them
        my_shootingData = self.shooting_data[['ID', 'Police Beats']]
        # similar key names
        my_shootingData = my_shootingData.rename(columns={"Police Beats":"beat_no"})
        # replaces all the NaN's with 0's to avoid an error when I set the type
        my_shootingData = my_shootingData.fillna(0)
        # sets both the keys to the same datatype before I join them 
        beat_filter["beat_no"] = beat_filter["beat_no"].astype(int) 
        my_shootingData["beat_no"] = my_shootingData["beat_no"].astype(int)
        # left joins  
        shoot_per_beat = beat_filter.merge(my_shootingData, on='beat_no', how='left')
        # groups unique values of shooting ID's by their beat, but accidentally removes the geometries. 
        shoot_per_beat = shoot_per_beat.groupby(by='beat_no', as_index=False).agg({'ID': pd.Series.nunique})
        # creates a just beat-to-geometry dataset from the base
        beat_geos = self.beat_master[['beat_no', 'geometry']].copy()
        # rejoins the shootings by their geometries 
        # needed to merge beat_geos to shoot_per_beat because the result wasn't a geopandas
        shoot_per_beat = beat_geos.merge(shoot_per_beat, on='beat_no', how='left')
        # renamed field name to make distinction easier
        shoot_per_beat = shoot_per_beat.rename(columns={'ID':'count_shootings'})
        return shoot_per_beat
    
    def gen_beats(self, df, community, lob, index_counter):
        for b in lob:
            # generates the row
            new_row = pd.DataFrame({"Community": community,
                    "beat_no": b}, index=[index_counter])
            # adds it to the dataframe
            df = df.append(new_row)
            index_counter = index_counter+1
        return df
    
    def outreach_assembly(self):
        # list of beats matched to communities
        austin_beats = [99, 97, 137, 143, 90, 81, 84, 85, 69, 68, 67, 70, 154, 145, 196, 183, 195]
        eastGarfield_beats = [82, 86, 140, 123, 77, 138, 146]
        englewood = [261, 135, 203, 202, 201, 215, 214, 210, 229]
        humboltPark_beats = [171, 190, 193, 194, 195, 68, 66, 65, 64, 80, 82]
        northLawndale_beats = [161, 130, 152, 109, 156, 153, 155, 142, 141, 140]
        southLawndale_beats = [167, 166, 160, 159, 151]
        westEnglewood_beats = [270, 164, 266, 205, 204, 203, 202, 7, 216]
        westGarfield_beats = [68, 90, 83, 100, 142, 82, 141]

        # I'm just aggregating the outreach workers like Sush recommended
        my_outreachData = self.outreach_data[['Community','Jun-19']]
        # replaces all the NaN's with 0's to avoid an error when I set the type
        my_outreachData = my_outreachData.fillna(0)
        # uses boolean indexing to identify like-columns and aggregate their results
        # get unique values:
        loc = my_outreachData.Community.unique()
        df = my_outreachData
        fields = ['Community', 'num_workers']
        agg_outreachData = pd.DataFrame(columns=fields)
        counter = 0
        for c in loc:
            # needed for the index
            # returns an integer
            df_value = df.loc[df['Community'] == c, 'Jun-19'].sum()
            if df_value > 0:
            # generates the row
                if c == 'Austin':
                    df_value = df_value/len(austin_beats)
                if c == 'East Garfield Park':
                    df_value = df_value/len(eastGarfield_beats)
                if c == 'Englewood':
                    df_value = df_value/len(englewood)
                if c == 'Humbolt Park':
                    df_value = df_value/len(humboltPark_beats)
                if c == 'North Lawndale':
                    df_value = df_value/len(northLawndale_beats)
                if c == 'South Lawndale':
                    df_value = df_value/len(southLawndale_beats)
                if c == 'West Englewood':
                    df_value = df_value/len(westEnglewood_beats)
                if c == 'West Garfield Park':
                    df_value = df_value/len(westGarfield_beats)
                new_row = pd.DataFrame({"Community": c,
                            "num_workers": df_value}, index=[counter])
                # adds it to the dataframe
                agg_outreachData = agg_outreachData.append(new_row)
                counter = counter+1
        my_outreachData = agg_outreachData

        columns = ['Community', 'beat_no']
        df_beats = pd.DataFrame(columns=columns)
        df_beats

        # uses function to build dataset
        my_counter = 0
        df = self.gen_beats(df_beats, "Austin", austin_beats, my_counter)
        my_counter = 17
        df = self.gen_beats(df, "East Garfield Park", eastGarfield_beats, my_counter)
        my_counter = 24
        df = self.gen_beats(df, "Englewood", englewood, my_counter)
        my_counter = 33
        df = self.gen_beats(df, "Humbolt Park", humboltPark_beats, my_counter)
        my_counter = 44
        df = self.gen_beats(df, "North Lawndale", northLawndale_beats, my_counter)
        my_counter = 54
        df = self.gen_beats(df, "North Lawndale", northLawndale_beats, my_counter)
        my_counter = 64
        df = self.gen_beats(df, "South Lawndale", southLawndale_beats, my_counter)
        my_counter = 69
        df = self.gen_beats(df, "West Englewood", westEnglewood_beats, my_counter)
        my_counter = 78
        df = self.gen_beats(df, "West Garfield Park", westGarfield_beats, my_counter)
        outreach_per_beat = my_outreachData.merge(df, on='Community', how='left')
        outreach_per_beat.drop_duplicates(subset ="beat_no", inplace = True)
        outreach_per_beat = outreach_per_beat.drop(33)
        outreach_per_beat = outreach_per_beat.drop(columns='Community')
        return outreach_per_beat
    
    def edge_assembly(self):
        edges = self.edge_data[['beat_no', 'edges w/ top 10 both']].copy()
        edges = edges.rename(columns={"edges w/ top 10 both":"edges"})
        divider = edges['edges'][277]
        divider = float(divider)
        edges = edges.drop(277)
        edges['edges'] = edges['edges']*divider
        edges['beat_no'] = edges['beat_no'].astype('int')
        return edges