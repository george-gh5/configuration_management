# Как устроен менеджер проектов

import importlib.metadata

package_name = "matplotlib"

requires = importlib.metadata.requires(package_name)

print("Dependencies for", package_name)
if requires:
    for dep in requires:
        print(" -", dep)
else:
    print("No dependencies listed")
