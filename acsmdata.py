import matplotlib.pyplot as plt
import pandas as pd

class ACSMdata():
    def __init__(self,path):
        self.path = path
        #import raw dataframe and stored as self.df
        self.df = pd.read_csv(path)

        #convert time index to pandas time stamp
        self.df['time_index'] = pd.to_datetime(self.df['time_index'])
        #convert all except for time into numbers
        self.df = self.df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name != 'time_index' else x)

    def printDF(self):
        print(self.df)
         
    def plotMZ(self, mz , ylim = None, limits = None):
        mzcolumnname = "'m/Q " + str(mz) + "'"
        if limits is not None:
            start = pd.to_datetime(limits[0])
            end = pd.to_datetime(limits[1])
            df = self.df[((self.df['time_index'] > start) & (self.df['time_index'] < end))]
        else:
            df = self.df

        plt.figure()
        plt.plot(df['time_index'],df[mzcolumnname])
        plt.xlabel('Time')
        if ylim != None:
            plt.ylim([ylim[0],ylim[1]])