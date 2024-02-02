from wrapper import wrap_plot


def plot_lang_dist():
    lang_dist = {
        'Japanese': 819405, 'English': 301087, 'Indonesian': 4588, 'Cantonese': 162388, 'Russian': 4294, 'German': 1584, 'Arabic': 6947, 'Korean': 13708,
        'Spanish': 7939, 'Tamil': 189, 'Portuguese': 2536, 'hun': 324, 'dan': 48, 'Italian': 2590, 'French': 3143, 'Chinese': 4151, 'ron': 666,
        'tha': 2033, 'nob': 165, 'pol': 305, 'als': 50, 'bul': 531, 'heb': 1355, 'ell': 944, 'tur': 641, 'hin': 247,
        'nld': 437, 'mkd': 93, 'ukr': 609, 'hrv': 217, 'urd': 87, 'bos': 103, 'khk': 256, 'lit': 198, 'ces': 138,
        'srp': 136, 'glg': 24, 'swe': 50, 'fin': 35, 'mal': 75, 'ben': 94, 'tel': 9, 'pes': 128, 'oci': 58, 'lvs': 25,
        'vie': 97, 'cat': 56, 'mar': 37, 'slv': 31, 'est': 2, 'hye': 12, 'zsm': 3, 'slk': 16, 'azj': 5, 'isl': 4,
        'ory': 6, 'pan': 3, 'bod': 2
    }


    lang_dist = dict(sorted(lang_dist.items(), key=lambda item: item[1]))

    wrap_plot(
        list(lang_dist.keys())[len(lang_dist.keys()) - 10:],
        list(lang_dist.values())[len(lang_dist.keys()) - 10:],
        plot_type="bar", color="orange"
    )


if __name__ == '__main__':
    plot_lang_dist()
