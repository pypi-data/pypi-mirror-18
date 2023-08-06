

import sys
import os

from cellpy import cellreader, dbreader, prmreader, filefinder

print "UNDER DEVELOPMENT"
prm_file = r"..\parametres\_cellpy_prms_jpm.ini"

print "Reading parametres"
prms = prmreader.read(prm_file)
print prms
excel_reader = dbreader.reader(prm_file=prm_file)
b_name = "e002_screen_printed"
serial_numbers = excel_reader.select_batch(b_name,5)
print " - serial_numbers: "
print serial_numbers
out_dir = r"C:\Cell_data\tmp"

cell_data_dict = {}
for n in serial_numbers:
    my_run_name = excel_reader.get_cell_name(n)
    print "\n - processing: %s" % (my_run_name)
    mass = excel_reader.get_mass(n)
    rawfiles, cellpyfile = filefinder.search_for_files(my_run_name, prm_filename=prm_file)
    print "   mass: %f" % (mass)
    cell_data_dict[my_run_name] = [mass, rawfiles, cellpyfile]
    print "   cellpyfile:", cellpyfile

    cell_data = cellreader.cellpydata()
    try:
        cell_data.loadcell(raw_files=rawfiles, cellpy_file=cellpyfile, mass=mass)
        if not cell_data.summary_exists:
            cell_data.make_summary()
            cell_data.save_test(cellpyfile)
        cell_data_dict[my_run_name].append(True)
    except IOError as e:
        print "ERROR - Could not load (IOError)"
        print e
        cell_data_dict[my_run_name].append(False)
    except MemoryError as e:
        print "ERROR - Could not load (MemoryError)"
        print e
        cell_data_dict[my_run_name].append(False)

for x,y in cell_data_dict.iteritems():
    print x, y
