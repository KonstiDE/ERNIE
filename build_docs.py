import csv
import os
import joblib

import config.config as cfg

from models.document import Document

from tqdm import tqdm


def extract_local(chunk_content, csv_file):

    r = 1
    for row in chunk_content:
        doc = Document(
            location=row[0],
            location_result_count=row[1],
            long=row[3],
            lat=row[2],
            url=row[4],
            img_url=row[5],
            src_file=csv_file,
            src_line=r,
            title=row[6]
        )
        res = doc.extract()
        if res:
            doc.save_document()
        r += 1


def build_docs(fetching_chunk_size=32):
    csvs_about = os.listdir(cfg.gdelt_src())

    loop = tqdm(csvs_about)

    for csv_file in loop:
        with open(os.path.join(cfg.gdelt_src(), csv_file)) as f:
            loop.set_postfix_str(csv_file.removesuffix(".csv"))

            try:
                csv_content = csv.reader(f, delimiter=",")
                next(csv_content)
                csv_content = list(csv_content)

                chunk_size = fetching_chunk_size
                chunks = [csv_content[x:x + chunk_size] for x in range(0, len(csv_content), chunk_size)]

                joblib.Parallel(n_jobs=len(chunks))(
                    joblib.delayed(extract_local)(chunk_content, csv_file.removesuffix(".csv")) for chunk_content in chunks)
            except StopIteration as _:
                pass


if __name__ == '__main__':
    build_docs()
