import numpy as np
from table import Table

class PlanetTable(Table):

    def __init__(self, verbose = 1):
        super().__init__(verbose)
        self.type = 'planets'
        return

    @classmethod
    def getKwords(cls):
        # dictionary of old: new keywords for planet quantities
        kwords = {
            'pl_name' : 'name',
            'sy_pnum' : 'planet_count',
            'disc_year' : 'year_discovered',
            'pl_controv_flag' : 'disputed_flag',
            'pl_orbper' : 'period',
            'pl_rade' : 'radius',
            'pl_bmasse' : 'mass',
            'pl_orbeccen' : 'eccentricity',
            'pl_orbsmax' : 'smax',
            'hostname' : 'star_name',
            'sy_snum' : 'star_count',
            'st_mass' : 'star_mass',
            'st_teff' : 'temperature',
            'sy_kmag' : 'mag',
            'st_logg' : 'logg',
            'st_rad' : 'star_radius',
            'st_met' : 'metallicity',
            'st_spectype' : 'spectral_type',
            'st_metratio' : 'metallicity_def'
        }

        return kwords
    
    
    ######### METHODS TO WINNOW DATA ########################
    
    def magCut(self, mag_kepler_lim = (-np.inf, 15)):
        self.winnow('mag', mag_kepler_lim, 'magnitude')
        return

    def tempCut(self, teff_lim = (4100, 6100)):
        self.winnow('temperature', teff_lim, 'effective temperature')
        return
    
    def loggCut(self, logg_lim = (4, 4.9)):
        self.winnow('logg', logg_lim, 'log(g)')
        return
    
    def periodCut(self, p_lim = (0, 50)):
        self.winnow('period', p_lim, 'period')
        return
    
    def radiusCut(self, r_lim = (2,32)):
        self.winnow('radius', r_lim, 'planetary radius')
        return

class CandidateTable(PlanetTable):
    def __init__(self, verbose=1):
        super().__init__(verbose)
        self.type = 'candidates'
        return
    
    def getKwords(self):
        # dictionary of old: new keywords for candidate quantities

        kwords = {
            'kepid' : 'id',
            'koi_score' : 'score',
            'koi_period' : 'period',
            'koi_prad' : 'radius',
            'koi_slogg' : 'logg',
            'koi_steff' : 'temperature',
            'koi_srad' : 'star_radius',
            'koi_model_snr' : 'snr',
            'koi_kepmag' : 'mag',
            'koi_smet' : 'metallicity'
        }
        return kwords
    
if __name__ == '__main__':
    print('CONFIRMED PLANETS TEST')
    planets = PlanetTable()
    planets.loadTable('confirmed.tbl')
    planets.magCut()
    planets.tempCut()
    planets.loggCut()
    planets.periodCut()
    planets.radiusCut()
    print('CANDIDATE PLANETS TEST')
    candidates = CandidateTable()
    candidates.loadTable('candidate.tbl')
    candidates.magCut()
    candidates.tempCut()
    candidates.loggCut()
    planets.periodCut()
    planets.radiusCut()


