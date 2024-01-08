import csv
import os
import joblib

import config.config as cfg

from models.document import Document

from tqdm import tqdm


def extract_local(chunk_content):
    for row in chunk_content:

        doc = Document(
            location=row[0],
            location_result_count=row[1],
            long=row[3],
            lat=row[2],
            url=row[4],
            img_url=row[5],
            title=row[5],
            date=csv_file.removesuffix(".csv")
        )
        doc.extract()
        doc.save_document()


if __name__ == '__main__':
    csvs_about = os.listdir(cfg.gdelt_path_about())

    loop = tqdm(range(len(csvs_about)))

    for i in loop:
        csv_file = csvs_about[i]

        with open(os.path.join(cfg.gdelt_path_about(), csv_file)) as f:
            loop.set_postfix_str(csv_file.removesuffix(".csv"))

            csv_content = csv.reader(f, delimiter=",")
            next(csv_content)
            csv_content = list(csv_content)

            chunk_size = 50
            chunks = [csv_content[x:x + chunk_size] for x in range(0, len(csv_content), chunk_size)]

            joblib.Parallel(n_jobs=len(chunks))(joblib.delayed(extract_local)(chunk_content) for chunk_content in chunks)
