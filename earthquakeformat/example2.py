from earthquakeformat import CSMIPVolume2Record
import os.path

s = CSMIPVolume2Record('test2.V2')

# --- This block of commands export acceleration data from all channels to CSV format
basename = 'CE1430V2_ACC_'
channelnumber = 0

# From each channel, get (#data points, time step) and check that they're all the same.
vals=[(e['info']['int_numv2accdpts'][1], e['info']['dbl_avgdt'][1]) for e in s.channels]
assert len(set(vals)) == 1, 'All channels do not have the same number of acceleration points. Quitting...'
nptsa = vals[0][0]
dt = vals[0][1] * 1.0E-3         # In milliseconds, so needs to be multiplied by 1E-3

file = open(basename+'{0}'.format(channelnumber)+'.csv', 'w')
header = 'Time (s),'+''.join(['Channel {0:02d} Acceleration (cm/s2),'.format(e) for e in range(len(s.channels))])+'\n'
file.write(header)
for i in range(nptsa):
    line = '{0},'.format(i * dt)+''.join(['{0},'.format(e['adata'][i]) for e in s.channels])+'\n'
    file.write(line)
file.close()
# ---
