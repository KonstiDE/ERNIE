from wrapper import wrap_plot


def plot_lang_dist():
    lang_dist_about_from = {
        'Japanese': 819405 + 1138368, 'English': 301087 + 323155, 'Indonesian': 4588, 'Cantonese': 162388 + 162125,
        'Russian': 4294, 'German': 1584 + 23, 'Arabic': 6947, 'Korean': 13708 + 2105, 'Spanish': 7939 + 4301,
        'Tamil': 189, 'Portuguese': 2536 + 269, 'hun': 324, 'dan': 48, 'Italian': 2590, 'French': 3143 + 1492,
        'Chinese': 4151, 'ron': 666, 'tha': 2033, 'nob': 165, 'pol': 305, 'als': 50, 'bul': 531, 'heb': 1355,
        'ell': 944, 'tur': 641, 'hin': 247, 'nld': 437, 'mkd': 93, 'ukr': 609 + 220, 'hrv': 217, 'urd': 87, 'bos': 103,
        'khk': 256, 'lit': 198, 'ces': 138, 'srp': 136, 'glg': 24, 'swe': 50, 'fin': 35, 'mal': 75, 'ben': 94, 'tel': 9,
        'pes': 128, 'oci': 58, 'lvs': 25, 'vie': 97, 'cat': 56, 'mar': 37, 'slv': 31, 'est': 2, 'hye': 12, 'zsm': 3,
        'slk': 16, 'azj': 5, 'isl': 4, 'ory': 6, 'pan': 3, 'bod': 2
    }

    lang_dist_noto = {
        'Chinese': 2509, 'Greek': 1236, 'Indonesian': 794, 'Kiluba': 16, 'hrv': 231, 'English': 9464, 'German': 1077,
        'Italian': 808, 'Polish': 213, 'Slovenian': 74, 'guj': 34, 'Japanese': 1247, 'Arabic': 648, 'hye': 27,
        'Russian': 844, 'Spanish': 2492, 'French': 815, 'Thai': 218, 'Korean': 1594, 'npi': 37, 'Ukrainian': 198,
        'Finnish': 128, 'Bosnian': 350, 'tur': 685, 'lit': 96, 'ron': 421, 'bul': 254, 'als': 290, 'por': 666,
        'swe': 154, 'mar': 54, 'ben': 152, 'urd': 43, 'zho': 238, 'mal': 140, 'nld': 93, 'hun': 163, 'heb': 75,
        'mkd': 137, 'nob': 101, 'hin': 185, 'cat': 33, 'srp': 80, 'pes': 33, 'tam': 61, 'khk': 18, 'azj': 70, 'slk': 59,
        'vie': 27, 'dan': 50, 'ces': 83, 'zsm': 39, 'est': 8, 'kaz': 5, 'lvs': 29, 'kan': 18, 'swh': 10,
        'tel': 26, 'pan': 12, 'sin': 6, 'isl': 23, 'afr': 4, 'som': 4, 'oci': 2, 'nno': 1, 'glg': 1
    }

    lang_dist = dict(sorted(lang_dist_noto.items(), key=lambda item: item[1]))

    wrap_plot(
        list(lang_dist.keys())[len(lang_dist.keys()) - 10:],
        list(lang_dist.values())[len(lang_dist.keys()) - 10:],
        plot_type="bar", color="orange", grid="-"
    )


if __name__ == '__main__':
    plot_lang_dist()
