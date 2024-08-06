import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ACSMdata():
    def __init__(self,path):
        self.path = path
        #import raw dataframe and stored as self.df
        self.df = pd.read_csv(path)

        self.mzs = np.arange(4,242,1)

        #convert time index to pandas time stamp
        self.df['time_index'] = pd.to_datetime(self.df['time_index'])
        #convert all except for time into numbers
        self.df = self.df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name != 'time_index' else x)

        print('Imported DataFrame.')
        print('')

        contains_nan = pd.isna(self.df).values.any()
        if contains_nan:
            self.df_withnan = self.df.copy(deep=True)
        
            # Identify rows with any NaN values
            rows_with_na = self.df.index[self.df.isna().any(axis=1)]

            # Drop rows with any NaN values
            self.df = self.df.dropna()

            self.df = self.df.reset_index()
            self.df = self.df.drop(columns=['index'])

            # Print the indices of rows that are dropped
            print("Rows dropped because of NaN:")
            print(self.df_withnan['time_index'][rows_with_na])

    def printDF(self):
        print(self.df)
         
    def plotIndMZ(self, mz , ylim = None, tlim = None):
        mzcolumnname = "'m/Q " + str(mz) + "'"
        if tlim is not None:
            start = pd.to_datetime(tlim[0])
            end = pd.to_datetime(tlim[1])
            df = self.df[((self.df['time_index'] > start) & (self.df['time_index'] < end))]
        else:
            df = self.df

        plt.figure()
        plt.plot(df['time_index'],df[mzcolumnname])
        plt.xlabel('Time')
        if ylim != None:
            plt.ylim([ylim[0],ylim[1]])

    def plotTotalMass(self, excludedmzs = None, ylim = None, tlim = None):
        if tlim is not None:
            start = pd.to_datetime(tlim[0])
            end = pd.to_datetime(tlim[1])
            df_slice = self.df.loc[((self.df['time_index'] > start) & (self.df['time_index'] < end))]
        else:
            df_slice = self.df

        y = np.zeros(len(df_slice))
        for idx, row in df_slice.iterrows():
            for mz in self.mzs:
                columnname = "'m/Q " + str(mz) + "'"
                if excludedmzs is None:
                    y[idx] = y[idx] + row[columnname]*mz
                else:
                    if mz not in excludedmzs:
                        y[idx] = y[idx] + row[columnname]*mz

        plt.figure()
        plt.plot(df_slice['time_index'],y)
        plt.xlabel('Time')
        if ylim != None:
            plt.ylim([ylim[0],ylim[1]])


    def plotAveSpectrum(self, mzlim = None, ylim = None, tlim = None):
        if tlim is not None:
            start = pd.to_datetime(tlim[0])
            end = pd.to_datetime(tlim[1])
            df_slice = self.df.loc[((self.df['time_index'] > start) & (self.df['time_index'] < end))]
        else:
            df_slice = self.df
            
        y = np.zeros(len(self.mzs))
        for idx, mz in enumerate(self.mzs):
            columnname = "'m/Q " + str(mz) + "'"
            y[idx] = np.mean(df_slice[columnname])*mz

        plt.figure()
        plt.bar(self.mzs,y)
        plt.ylabel('Relative Abundance')
        plt.xlabel('m/z')
        if mzlim is not None:
            plt.xlim([mzlim[0],mzlim[1]])
        if ylim is not None:
            plt.ylim([ylim[0],ylim[1]])



        

