from wrapper import wrap_plot


def plot_lang_dist():
    lang_dist = {
        'Japanese': 943685, 'English': 284204, 'Indonesian': 4268, 'Chinese (Simp)': 21092, 'Russian': 4288, 'de': 957,
        'Hindi': 24558,
        'Chinese': 23150, 'Arabic': 7230, 'Korean': 10457, 'Spanish': 8074, 'ta': 189, 'pt': 2397, 'hu': 320, 'da': 75,
        'it': 2594, 'fr': 3144, 'ro': 685, 'th': 2032, 'no': 166, 'pl': 306, 'sq': 46, 'bg': 532, 'iw': 1279,
        'el': 941, 'tr': 645, 'nl': 436, 'mk': 93, 'uk': 523, 'kk': 13, 'sr': 263, 'ur': 98, 'mn': 288,
        'lt': 189, 'cs': 138, 'hr': 199, 'vo': 22, 'gl': 24, 'sv': 50, 'fi': 52, 'ml': 75, 'bn': 93, 'te': 9,
        'fa': 126, 'ba': 14, 'lv': 25, 'crs': 23, 'hy': 26, 'vi': 74, 'mr': 37, 'sl': 31, 'et': 2, 'un': 31,
        'ms': 3, 'ca': 19, 'sk': 14, 'az': 5, 'is': 4, 'tt': 2, 'zzp': 1, 'pa': 3, 'nn': 1
    }

    lang_dist = dict(sorted(lang_dist.items(), key=lambda item: item[1]))

    wrap_plot(
        list(lang_dist.keys())[len(lang_dist.keys()) - 10:],
        list(lang_dist.values())[len(lang_dist.keys()) - 10:],
        plot_type="bar", color="orange", grid="--"
    )


if __name__ == '__main__':
    plot_lang_dist()
