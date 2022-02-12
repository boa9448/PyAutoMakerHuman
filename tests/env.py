import os
import sys

root_dir = os.path.abspath(os.path.join(__file__, "..", ".."))

test_img_dir = os.path.join(root_dir, "tests", "imgs")
train_dataset_dir = os.path.join(root_dir, "dataset")
package_dir = os.path.join(root_dir, "src")

sys.path.append(package_dir)