import csv
import os
import joblib

import config.config as cfg

from models.document import Document

from tqdm import tqdm


def extract_local(chunk_content, csv_file):
    for row in chunk_content:

        doc = Document(
            location=row[0],
            location_result_count=row[1],
            long=row[3],
            lat=row[2],
            url=row[4],
            img_url=row[5],
            title=row[6],
            date=csv_file.removesuffix(".csv")
        )
        doc.extract()
        doc.save_document()


def build_docs(fetching_chunk_size=32):
    csvs_about = os.listdir(cfg.gdelt_path_about())

    loop = tqdm(range(len(csvs_about)))

    for i in loop:
        csv_file = csvs_about[i]

        with open(os.path.join(cfg.gdelt_path_about(), csv_file)) as f:
            loop.set_postfix_str(csv_file.removesuffix(".csv"))

            try:
                csv_content = csv.reader(f, delimiter=",")
                next(csv_content)
                csv_content = list(csv_content)

                chunk_size = fetching_chunk_size
                chunks = [csv_content[x:x + chunk_size] for x in range(0, len(csv_content), chunk_size)]

                joblib.Parallel(n_jobs=len(chunks))(
                    joblib.delayed(extract_local)(chunk_content, csv_file) for chunk_content in chunks)
            except StopIteration as _:
                pass


if __name__ == '__main__':
    build_docs()
