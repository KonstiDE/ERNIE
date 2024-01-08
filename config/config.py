import os.path

cfg = {
    "base_path": "/home/s371513/ernie",
    "gdelt_about_src": "data/about/gdelt/",
    "gdelt_from_src": "data/from/gdelt/",
    "gdelt_about_out": "data/out/about/",
    "gdelt_from_out": "data/out/from/",
    "warn_earthquakes_src": "data/earthquakes/"
}

def gdelt_path_about():
    return os.path.join(cfg["base_path"], cfg["gdelt_about_src"])

def gdelt_path_from():
    return os.path.join(cfg["base_path"], cfg["gdelt_from_src"])

def gdelt_out_path_about():
    return os.path.join(cfg["base_path"], cfg["gdelt_about_out"])

def gdelt_out_path_from():
    return os.path.join(cfg["base_path"], cfg["gdelt_from_out"])

def warn_path_earthquakes():
    return os.path.join(cfg["base_path"], cfg["warn_earthquakes_src"])