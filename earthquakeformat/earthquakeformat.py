"""
Module for handling CSMIP standard tape format files

class Volume2Record reads files with extensions V2 downloaded from strongmotioncenter.org or similar websites.

The format specifications file, 'Standard Tape Format for CSMIP Strong-Motion Data Types'
is located at:
http://www.strongmotioncenter.org/NCESMD/reports/DMGformat85.pdf

This requires a helper file, typically named "earthquakeschema.py"

TODO: Add method to convert to SMC file
TODO: Add SMC record classes

"""

__author__ = "Pinaky Bhattacharyya"
__status__ = 'Beta'


from earthquakeschema import v2th
from earthquakeschema import v2ih
from earthquakeschema import v2rh


# This class stores information from a CSMIP V2 file containing displacement, velocity and acceleration data.
class CSMIPVolume2Record:
    def __init__(self, fname):
        self.filename = fname   # Store the filename for the user's reference
        self.channels = []
        f = open(fname, 'r')

        txtheader = {}
        intheader = {}
        dblheader = {}

# doneflag lets this constructor know when the
        doneflag = False
        channelcount = 0
# This outermost loop runs as long as there are lines to read in the input file.
        while not doneflag:
            channelcount += 1
            c = 0
            for line in f:
                if (c == 0) and (line == ''):
                    doneflag = True
                    break
                c += 1
# The first 25 lines are the text header. Read it in if the file is at that position.
                if c in range(1, 26):
                    for e in v2th:
                        if e[0] == c:
                            if e[2] != -1:
                                txtheader[e[3]] = (e[4], line[(e[1] - 1):e[2]])
                            else:
                                txtheader[e[3]] = (e[4], line)
# The next lines 26 to 32 consist of fixed-width integers for the integer header.
                elif c in range(26, 33):
                    for e in v2ih:
                        if e[1] == c:
                            intheader[e[4]] = (e[5], int(line[(e[2] - 1):e[3]].strip()))
# The last lines 33 to 45 consist of fixed-width real data.
                elif c in range(33, 46):
                    for e in v2rh:
                        if e[1] == c:
                            dblheader[e[4]] = (e[5], float(line[(e[2] - 1):e[3]].strip()))

                elif c >= 46:
                    break

            if (c == 0) or doneflag:
                break
# From the integer header info, read the size of the acc, vel, dsp arrays as nptsa, nptsv, nptsd
            nptsa = intheader['int_numv2accdpts'][1]
            nptsv = intheader['int_numvelpts'][1]
            nptsd = intheader['int_numdispts'][1]
# Initialize lists with the data sizes in hand
            adata = nptsa * [None]
            vdata = nptsv * [None]
            xdata = nptsd * [None]

# Now, 3 loops for reading acceleration, velocity and displacement data
# Data is formated in floating point of width 10, so break each line of size 80 chars into chunks of size 10.
# Append to the array storing the data and keep a running counter to make sure you stop at the right point (c==npts*).


# Loop 1: Read in acceleration data
            c = 0
            bflag = False
            while not bflag:
                line = f.readline()
                for i in range(0, 80, 10):
                    c += 1
                    adata[c-1] = float(line[i:(i+10)])
                    if c == nptsa:
                        bflag = True
                        break
            assert c == nptsa, "Failed acceleration data point count. Info: {0}, {1}".format((c, nptsa))
# Skip the line at the beginning of the data array that says:
# @@@@@ points of @@@@@ data equally spaced at  @@@@ @@@, in @@.      (@@@@@)
            line = f.readline()

# Loop 2: Read in velocity data
            c = 0
            bflag = False
            while not bflag:
                line = f.readline()
                for i in range(0, 80, 10):
                    c += 1
                    vdata[c-1] = float(line[i:(i+10)])
                    if c == nptsv:
                        bflag = True
                        break
            assert c == nptsv, "Failed velocity data point count. Info: {0}, {1}".format((c, nptsv))
            line = f.readline()

# Loop 3: Read in displacement data
            c = 0
            bflag = False
            while not bflag:
                line = f.readline()
                for i in range(0, 80, 10):
                    c += 1
                    xdata[c-1] = float(line[i:(i+10)])
                    if c == nptsd:
                        bflag = True
                        break
            assert c == nptsd, "Failed displacement data point count. Info: {0}, {1}".format((c, nptsd))
            line = f.readline()

# Update some lines in the text header whose lengths needed to be determined from the integer header.
# Example: earthquake name, station name, lilt line
            txtheader['txt_eqname'] = txtheader['txt_eqname'][0:intheader['int_numleteqname'][1]]
            txtheader['txt_stnname'] = txtheader['txt_stnname'][0:intheader['int_numletstname'][1]]
            txtheader['txt_eqtiltline'] = txtheader['txt_eqtiltline'][0:intheader['int_numleteqtitl'][1]]

# Prepare the data for storage in the channel dictionary
            info = txtheader.copy()
            info.update(intheader)
            info.update(dblheader)

# Add meta-data 'info', as well as actual data 'adata', 'vdata', 'xdata' to the channel array
            self.channels.append({'info': info, 'adata': adata, 'vdata': vdata, 'xdata': xdata})

# We are done with the input file, so close it
        f.close()
# Store the number of channels
        self.channelcount = channelcount - 1

#
    def converttomat(self, fname, nameprefix=None):
        import scipy.io

        if nameprefix is None:
            nameprefix = ''

        scipy.io.savemat(fname, {nameprefix + 'channel{0:02d}'.format(ch['info']['int_accchnnum'][1]): {'adata': ch['adata'], 'vdata': ch['vdata'], 'xdata': ch['xdata'], 'info': ch['info']} for ch in self.channels})

    #def converttosmc(self, fname):
