# Script to remove from the clean folder all files not present in html folder

from os import listdir, remove
from os.path import isfile, join

html_files = [f for f in listdir('./html/') if isfile(join('./html/', f))]
clean_files = [f for f in listdir('./clean/') if isfile(join('./clean/', f))]

counter = 0

for clean in clean_files:
    if clean not in html_files:
        remove('./clean/' + clean)
        counter += 1

print("Removed " + str(counter) + " files.")
