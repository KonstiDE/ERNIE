import trafilatura


def extract_main_text(doc):
    downloaded = trafilatura.fetch_url(doc.url)
    return trafilatura.extract(downloaded, include_comments=False), downloaded

