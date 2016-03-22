from earthquakeformat import CSMIPVolume2Record
import os.path

s = CSMIPVolume2Record('test2.V2')


# This command saves all channel information to 'CE1430V2.mat' in the
#   current working directory using a hardcoded helper function.
# Variables are stored as structures named '<nameprefix>_channel1', ..., '<nameprefix>_channel10', etc.
#   according to the prefix specified in the arguments to the 'converttomat' function.
fname = 'CE1430V2.mat'
if os.path.isfile(fname):
    input('File already exists. Press enter to overwrite or abort sequence (Ctrl+C in windows)... >> ')

s.converttomat(fname, nameprefix='case1_')
