import os
import sys

root_dir = os.path.abspath(os.path.join(__file__, ".."))
root_dir = os.path.split(root_dir)[0]

img_dir = os.path.join(root_dir, "tests", "imgs")
root_dir = os.path.join(root_dir, "src")

sys.path.append(root_dir)
print(root_dir)

from PyAutoMakerHuman.form import main

main.start_main()