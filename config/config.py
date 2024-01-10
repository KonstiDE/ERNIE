import os.path

cfg = {
    "base_path": "/home/s371513/ernie",
    "gdelt_src": "data/about/gdelt/",
    "gdelt_out": "data/out/about/",
    "warn_earthquakes_src": "data/earthquakes/",
    "warn_tsunamis_src": "data/tsunamis/",
    "warn_volcanos_src": "data/volcanos/"
}

def gdelt_src():
    return os.path.join(cfg["base_path"], cfg["gdelt_src"])

def gdelt_out():
    return os.path.join(cfg["base_path"], cfg["gdelt_out"])


# TODO: Paths below to be removed for the final pipe
def warn_path_earthquakes():
    return os.path.join(cfg["base_path"], cfg["warn_earthquakes_src"])

def warn_path_tsunamis():
    return os.path.join(cfg["base_path"], cfg["warn_tsunamis_src"])

def warn_path_volcanos():
    return os.path.join(cfg["base_path"], cfg["warn_volcanos_src"])