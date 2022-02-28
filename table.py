import numpy as np
from astropy.io import ascii

class Table():

    def __init__(self, verbose = 1):
        self.data = {}
        self.v = verbose
        self.mask = None
        self.count = 0
        self.type = ''
        return

    def loadTable(self, filepath, load_other = []):
        """
        Extracts the data from an astropy IPAC table and returns it
        as a dictionary, using keys that are a bit more informative
        than the astropy IPAC table about what the data stored is 
        supposed to be. It also reformats the data so that the errors
        are stored alongside their values, like [value, +err, -err].

        Args:
            filepath (str): path to IPAC table file. 

            load_other (optional, list): load in other values than the
                default ones defined in getKwords().
        """
        # read data in
        f = ascii.read(filepath)
        ipacKwords = list(f.columns)

        if self.v:
            print("column headers from IPAC table:")
            print(ipacKwords)
            print()

        # get the kword dictionary
        desired_kwords = self.getKwords()
        
        # iterate over the IPAC columns to save desired data
        for kw in ipacKwords:
            col_data = np.array(f[kw])
            # check if this value has errorbars
            if kw + 'err1' in ipacKwords:
                # assumes that other errorbar is in table,
                # stacks them into 2D array
                err1 = np.array(f[kw+'err1'])
                err2 = np.array(f[kw+'err2'])
                col_data = np.column_stack((col_data, err1, err2))
            
            # annoyingly the candidates table uses different naming
            # convention...
            elif kw + '_err1' in ipacKwords:
                err1 = np.array(f[kw+'_err1'])
                err2 = np.array(f[kw+'_err2'])
                col_data = np.column_stack((col_data, err1, err2))

            if kw in desired_kwords or kw in load_other:
                if kw in load_other:
                    save_name = kw
                else:
                    save_name = desired_kwords[kw]
                # if this is the first time loading this data,
                # initialize the data in the dict
                if not save_name in self.data:
                    self.data[save_name] = col_data
                
                # otherwise, append the data to the end of 
                # previous data
                else:
                    old_data = self.data[save_name]
                    self.data[save_name] = \
                            np.append(old_data, col_data, axis = 0)
                    

            
                # initialize the mask, used to make cuts to data
                self.mask = np.ones(np.max(self.data[save_name].shape), 
                        dtype = bool)
                self.count = np.max(self.data[save_name].shape)
        
        if self.v:
            print("loaded datasets:")
            print(list(self.data.keys()))
            print()
            print("number of %s loaded:"%self.type)
            print(np.sum(self.mask))
            print()
        return

    @classmethod
    def getKwords(cls):
        # passed to subclasses
        pass
    
    def getAllData(self):
        """
        Gets the loaded IPAC table, unmasked.

        Raises:
            ValueError: If no data is loaded, throws error.

        Returns:
            dict: IPAC data
        """
        if not self.data:
            raise ValueError("no data loaded.")
        
        return self.data
    
    def getMaskedData(self, key):
        data = self.getAllData()[key]

        if len(data.shape) == 2:
            return data[self.mask, :]
        else:
            return data[self.mask]
    
    def _applyLimits(self, data, limits):
        temp_mask = (data > limits[0]) \
                & (data < limits[1])
        return temp_mask
    
    def winnow(self, data_key, limits, name = '', apply_cut = None):
        if self.v:
            print('number of %s before %s cut:'%(self.type, name))
            print(np.sum(self.mask))
            print()
        
        # if apply_cut function is not passed, use default
        if apply_cut is None:
            apply_cut = self._applyLimits
       
        for_winnow = self.getAllData()[data_key]
        
        # check the shape of the data - if 2D than need a slice
        # to access just the values and not the errorbars too.
        if len(for_winnow.shape) == 2:
            slc = (slice(None), 0)
        else:
            slc = (slice(None))

        temp_mask = apply_cut(for_winnow[slc], limits)
        
        # if any data has failed this or prevous cuts,
        # should be/stay removed from analysis
        self.mask = temp_mask & self.mask

        if self.v:
            print('number of %s to fail %s cut:'%(self.type, name))
            print(self.count - np.sum(temp_mask))
            print('\nnumber of %s left:'%(self.type))
            print(np.sum(self.mask))
            print()

        return