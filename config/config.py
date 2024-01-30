import os.path

cfg = {
    "base_path": "/home/s371513/ernie",
    "gdelt_src": "data/from/gdelt/",
    "gdelt_out": "data/out/from/",
    "warn_earthquakes_src": "data/earthquakes/",
    "warn_tsunamis_src": "data/tsunamis/",
    "warn_volcanos_src": "data/volcanos/",
    "os_environs": {
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "CUDA_VISIBLE_DEVICES": "MIG-f29aed64-88d8-567c-9102-1b0a7b4e0b3a",
        " TOKENIZERS_PARALLELISM": "false"
    }
}


def base_path():
    return cfg["base_path"]


def gdelt_src():
    return os.path.join(cfg["base_path"], cfg["gdelt_src"])


def gdelt_out():
    return os.path.join(cfg["base_path"], cfg["gdelt_out"])


# TODO: Paths below to be removed for the final pipe
def warn_path_earthquakes():
    return (
        os.path.join(cfg["base_path"], cfg["warn_earthquakes_src"]))


def warn_path_tsunamis():
    return os.path.join(cfg["base_path"], cfg["warn_tsunamis_src"])


def warn_path_volcanos():
    return os.path.join(cfg["base_path"], cfg["warn_volcanos_src"])


def write_os_environments():
    for key, val in cfg["os_environs"].items():
        os.environ[key] = val
