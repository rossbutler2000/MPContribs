import os
import ase.db
import collections as coll

def run(mpfile):
    url = mpfile.hdata['_hdata']['url']
    # TODO
    # - extract db name from url -> dbfile = 'mp_gllbsc.db'
    # - check if mp_gllbsc.db exists
    dbfile = url.rsplit('/')[-1]
    con = ase.db.connect(dbfile)
    count = 0
    for row in con.select('mpid'):
        d = coll.OrderedDict([])
        d['kohn-sham_bandgap'] = coll.OrderedDict([])
        d['derivative_discontinuity'] = coll.OrderedDict([]) 
        d['quasi-particle_bandgap'] = coll.OrderedDict([])
        count = count + 1
        mpid = 'mp-' + str(row.mpid)
        d['kohn-sham_bandgap']['indirect'] = row.gllbsc_ind_gap - row.gllbsc_disc
        d['kohn-sham_bandgap']['direct'] = row.gllbsc_dir_gap - row.gllbsc_disc
        d['derivative_discontinuity'] = row.gllbsc_disc
        d['quasi-particle_bandgap']['indirect'] = row.gllbsc_ind_gap
        d['quasi-particle_bandgap']['direct'] = row.gllbsc_dir_gap
        mpfile.add_hierarchical_data(mpid,d) 
        if count == 10:
            break
    print mpfile

