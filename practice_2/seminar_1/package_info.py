# Как устроен менеджер проектов

import importlib.metadata

package_name = "matplotlib"

metadata = importlib.metadata.metadata(package_name)

print(f"Package: {metadata['Name']}")
print(f"Version: {metadata['Version']}")
print(f"Author: {metadata['Author']}")
