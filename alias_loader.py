import importlib.util
import sys
import pathlib

# Path to the real folder with underscores
project_path = pathlib.Path(__file__).resolve().parent / "alx_backend_caching_property_listings"
init_file = project_path / "__init__.py"

# Load real package as a "fake" alias (dash version)
spec = importlib.util.spec_from_file_location(
    "alx-backend-caching_property_listings",  # fake alias with dash
    str(init_file)
)
module = importlib.util.module_from_spec(spec)
sys.modules["alx-backend-caching_property_listings"] = module
spec.loader.exec_module(module)
