import importlib.util
import sys
import pathlib

# Path to the REAL Django project folder with the dash
project_path = pathlib.Path(__file__).resolve().parent / "alx-backend-caching_property_listings"

# Force it to be seen as a Python package
init_file = project_path / "__init__.py"
if not init_file.exists():
    init_file.touch()  # create empty if missing

# Load the "fake" valid alias name
spec = importlib.util.spec_from_file_location(
    "alx_backend_caching_property_listings",
    str(init_file)
)
module = importlib.util.module_from_spec(spec)
sys.modules["alx_backend_caching_property_listings"] = module
spec.loader.exec_module(module)
