from table import Table
import numpy as np
import h5py as hp

class StarTable(Table):

    def __init__(self, verbose=1):
        super().__init__(verbose)
        self.type = 'stars'
        return
    
    @classmethod
    def getKwords(cls):
        # dictionary of old: new keywords for star quantities
        kwords = {
            'id' : 'kepid',
            'teff' : 'temperature',
            'logg' : 'logg',
            'feh' : 'metallicity',
            'mass' : 'mass',
            'radius' : 'radius',
            'kepmag' : 'mag',
            'dist' : 'distance',
            'nkoi' : 'n_planets',
        }
        return kwords

    ########## HDF5 IO ####################################
    def saveData(self, savepath = 'stars.hdf5'):
        f = hp.File(savepath, 'w')
        data = self.getAllData()
        for dname, dset in data.items():
            f.create_dataset(dname, data=dset, 
                    compression = 'gzip', compression_opts = 9)
        f.close()
        return
    
    def loadHdf5(self, loadpath = 'stars.hdf5'):
        f = hp.File(loadpath, 'w')
        keylist = list(f.keys())
        for k in keylist:
            self.data[k] = f[k][:]
        f.close()
        return
    ######### METHODS TO WINNOW DATA ####################

    def _applyLimits(self, data, limits):
        temp_mask = (data > limits[0]) \
                & (data < limits[1])
        return temp_mask

    def magCut(self, mag_kepler_lim = (-np.inf, 15)):
        self.winnow('mag', mag_kepler_lim, 'magnitude')
        return

    def tempCut(self, teff_lim = (4100, 6100)):
        self.winnow('temperature', teff_lim, 'effective temperature')
        return
    
    def loggCut(self, logg_lim = (4, 4.9)):
        self.winnow('logg', logg_lim, 'log(g)')
        return



if __name__ == '__main__':
    stars = StarTable()
    stars.loadTable('supstars.tbl')
    stars.magCut()
    stars.tempCut()
    stars.loggCut()

