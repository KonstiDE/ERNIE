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
        'Tamil': 3836, 'Chinese': 14910, 'Japanese': 14533, 'Spanish': 10105, 'Turkish': 2720, 'English': 51589,
        'Italian': 4027,
        'Finnish': 610, 'French': 3945, 'German': 4383, 'Portuguese': 2734, 'Greek': 3680, 'kat': 31, 'hrv': 646,
        'Thai': 1361, 'als': 806, 'bul': 925, 'pol': 952, 'slv': 284, 'ron': 1933, 'kor': 10464,
        'guj': 63, 'hun': 951, 'ukr': 1353, 'zho': 1544, 'arb': 3042, 'hye': 272, 'srp': 268,
        'mal': 785, 'Russian': 3952, 'npi': 151, 'swe': 417, 'azj': 284, 'cat': 178, 'ben': 704, 'bos': 940,
        'hin': 605, 'ces': 590, 'nld': 567, 'lit': 420, 'nob': 282, 'heb': 434, 'mar': 150, 'urd': 125,
        'slk': 293, 'vie': 140, 'mkd': 417, 'tam': 225, 'lvs': 93, 'pes': 152, 'khk': 107, 'dan': 162,
        'zsm': 124, 'swh': 34, 'oci': 22, 'est': 41, 'kaz': 29, 'pan': 34, 'kan': 35, 'tel': 53,
        'sin': 40, 'afr': 9, 'isl': 62, 'glg': 7, 'som': 12, 'pcm': 1, 'nno': 3, 'krc': 1, 'chv': 1,
        'ast': 1
    }


    lang_dist = dict(sorted(lang_dist_noto.items(), key=lambda item: item[1]))

    wrap_plot(
        list(lang_dist.keys())[len(lang_dist.keys()) - 10:],
        list(lang_dist.values())[len(lang_dist.keys()) - 10:],
        plot_type="bar", color="orange", grid="-"
    )


if __name__ == '__main__':
    plot_lang_dist()
