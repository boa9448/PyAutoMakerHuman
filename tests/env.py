import os
import sys

root_dir = os.path.abspath(os.path.join(__file__, "..", ".."))

img_dir = os.path.join(root_dir, "tests", "imgs")
package_dir = os.path.join(root_dir, "src")

sys.path.append(package_dir)