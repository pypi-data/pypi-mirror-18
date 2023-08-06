import os.path
import jinja2
import numpy as np
from cpc.geofiles.loading import load_ens_fcsts
from cpc.geogrids import Geogrid
from cpc.mpp.cal import er
from cpc.stats.stats import put_terciles_in_one_array


# # Load raw forecast data
# issued_dates = ['20160101']
# fhrs = range(150, 264+1, 6)
# members = range(0, 20+1)
# file_template = '/Users/mike/Work/data/mpp/raw-fcst/gefs_{{yyyy}}{{mm}}{{dd}}_00z_f{{fhr}}_m{{' \
#                 'member}}.grb2'
# data_type = 'grib2'
# geogrid = Geogrid('1deg-global')
# grib_var = 'TMP'
# grib_level = '2 m above ground'
# raw_fcst = load_ens_fcsts(issued_dates, fhrs, members, file_template, data_type, geogrid,
#                           grib_level=grib_level, grib_var=grib_var)
# raw_fcst.ens.astype('float32').tofile('raw_fcst_ens.bin')
# raw_fcst.ens_mean.astype('float32').tofile('raw_fcst_ens_mean.bin')
# raw_fcst = type('', (), {})()
# raw_fcst.ens = np.fromfile('raw_fcst_ens.bin', dtype='float32').reshape(1, 21, 65160)[0]
# raw_fcst.ens_mean = np.fromfile('raw_fcst_ens_mean.bin', dtype='float32').reshape(1, 65160)
#
# # Load stats data
# stat_types = ['cov', 'es', 'xm', 'xv', 'ym', 'yv']
# stats = {}
# stats_file_tmpl = os.path.expandvars(os.path.expanduser('~/Work/data/mpp/stats/6-10day/{{'
#                                                         'stat}}_sm31d_0111.bin'))
# for stat in stat_types:
#     file = jinja2.Template(stats_file_tmpl).render(stat=stat)
#     stats[stat] = np.fromfile(file, dtype='float32')
#
# stats['num_stats_members'] = 11
# stats['num_fcst_members'] = 21
# stats['num_years'] = 24
# POE = er.regress(raw_fcst.ens, stats)
#
# from cpc.geogrids import Geogrid
# from cpc.geoplot import Geomap, Geofield
# from cpc.stats import poe_to_terciles
# from cpc.geoplot.colors import precip_terciles
# from cpc.geogrids.manipulation import smooth
#
# geogrid = Geogrid('1deg-global')
# levels = [-90, -80, -70, -60, -50, -40, -33, 33, 40, 50, 60, 70, 80, 90]
# ptiles = [1, 2, 5, 10, 15, 20, 25, 33, 40, 50, 60, 67, 75, 80, 85, 90, 95, 98, 99]
# b, n, a = poe_to_terciles(POE, ptiles)
# data = 100 * smooth(put_terciles_in_one_array(b, n, a).reshape(geogrid.num_y, geogrid.num_x),
#                     geogrid, 0.5)
# geofield = Geofield(data, geogrid, levels=levels, fill_colors=precip_terciles)
# geomap = Geomap(cbar_type='tercile')
# geomap.plot(geofield)
# geomap.save('test.png')

from cpc.geogrids import Geogrid
from cpc.geoplot import Geomap, Geofield

variable = 'tmean'

geogrid = Geogrid('1deg-global')

levels = {
    'tmean': {
        'a1': np.arange(0.9, 1.1, 0.01),
        'ebest': np.arange(2.5, 3.5, 0.01),
        'emean': np.arange(4, 5.01, 0.01),
        'k': np.arange(0.1, 1.1, 0.1),
        'rxy': np.arange(0.1, 1.1, 0.1),
        'es': np.arange(3, 28, 3),
        'yv': np.arange(5, 56, 5),
        'xv': np.arange(40, 50, 0.5),
        'rbest': np.arange(0, 1.3, 0.1),
        'y_anom_mean': 'auto',
	'y_anom_single': np.arange(-10, 16, 1),
    },
    'precip': {
        'a1': np.arange(0.1, 1.3, 0.1),
        'ebest': np.arange(0.5, 3, 0.2),
        'emean': np.arange(0.5, 3, 0.2),
        'k': np.arange(0.1, 1.1, 0.1),
        'rxy': np.arange(0.1, 1.1, 0.1),
        'es': np.arange(1, 11, 1),
        'yv': np.arange(1, 11, 1),
        'xv': np.arange(1, 11, 1),
        'rbest': np.arange(0, 1.3, 0.1),
        'y_anom_mean': 'auto',
	'y_anom_single': 'auto',
    }
}

for stat in ['xv', 'a1', 'ebest', 'emean', 'k', 'rxy', 'es', 'yv', 'rbest', 'y_anom_mean', 'y_anom_single']:
    # geomap = Geomap(domain='global', projection='mercator')
    # geofield = Geofield(locals()[stat], geogrid, levels=levels[stat])
    # geomap.plot(geofield)
    # geomap.save('{}.png'.format(stat), dpi=200)

    geomap = Geomap()
    geofield = Geofield(np.fromfile('{}-orig.bin'.format(stat), 'float32'), geogrid,
                        levels=levels[variable][stat])
    geomap.plot(geofield)
    geomap.save('{}-orig.png'.format(stat), dpi=200)
