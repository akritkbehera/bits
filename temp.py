from bits_helpers.utilities import getConfigPaths, getGeneratedPackages
import os
from os.path import exists

def checkForFilename(taps, pkg, d):
    print(f"[DEBUG] checkForFilename called with pkg={pkg}, d={d}")

    filename = taps.get(pkg, f"{d}/{pkg}.sh")
    print(f"[DEBUG] First candidate: {filename}")

    if not os.path.exists(filename):
        if "/" in pkg:
            filename = taps.get(pkg, f"{d}/{pkg}")
            print(f"[DEBUG] Second candidate (with '/'): {filename}")
        else:
            filename = taps.get(pkg, f"{d}/{pkg}/latest")
            print(f"[DEBUG] Second candidate (no '/'): {filename}")

    print(f"[DEBUG] Returning filename: {filename}, exists? {os.path.exists(filename)}")
    return filename

pkg = "py-flit-core.file"
configDir = "/home/akbehera/Bits/repositories/general.bits"
taps = {}
genPackages = getGeneratedPackages(configDir)

# Print all keys in genPackages that contain 'py-flit-core'
for k in genPackages:
    if 'py-flit-core' in k:
        print(f"genPackages key: {k}, value: {genPackages[k]}")

print("Config paths:", list(getConfigPaths(configDir)))
for d in getConfigPaths(configDir):
    fn = checkForFilename(taps, pkg, d)
    # print("Checking for:", fn)
    # print("Checking in", d)
    # print("Candidate filename:", fn)
    # print("Candidate filename:", fn, "exists?", os.path.exists(fn))
    # print("Candidate filename:", pkg, "exists?", os.path.exists(d))

