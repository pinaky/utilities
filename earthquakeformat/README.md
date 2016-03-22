This folder contains **unofficial**, **untested** utilities to read in and convert earthquake monitoring data files.

Currently, the readers are in the form of loose Python scripts. There is no installation script and they should be used directly.

Currently, only support for reading in CSMIP/CGS Volume 2 data is supported. SciPy conversion to the MAT file standard is available if you have access to SciPy on your Python installation.

NumPy and SciPy is easy enough to install on Linux with 'pip'.

For Windows and Mac OS X users, the Anaconda Python distribution includes SciPy. You will need this to export the data to MAT format.

Alternatively, 'example2.py' demonstrates how to export CSMIP/CGS Volume 2 data manually to CSV. You can then import the CSV in Octave.

List of files:
- earthquakeformat.py: This is the main library file from which you would need to import the relevant classes for reading earthquake data records. Currently, the only class is 'CSMIPVolume2Record'
- earthquakeschema.py: This is a support file used by earthquakeformat.py. Keep it in the same folder.
- example1.py: Example that demonstrates export of a CSMIP/CGS Vol 2 record
- example2.py: Example that demonstrates export of channel accelerations from a CSMIP/CGS Vol 2 Record

Earthquake records can be obtained from http://strongmotioncenter.org/

Stations on the CGS network record data in the format readable by the 'CSMIPVolume2Record' class.

Specifications of the format can be found at http://strongmotioncenter.org/aboutcesmd.html under the "Data Format" section.
