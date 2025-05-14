from glob import glob
import os

for f in glob('*'):
   print(f.split('-')[-1].strip())
   os.rename(f, f.split('-')[-1].strip())
