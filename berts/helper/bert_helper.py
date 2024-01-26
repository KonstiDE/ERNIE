def read_text(path: str):
    with open(path, "r") as f:
        all_together = f.read()
        doc_contents = all_together.split("\n~~~~~~~~~~~~~~~~caipi~~~~~~~~~~~~~~~~\n")

        file_names = [filename.split("~~~~~filename~~~~~")[0] for filename in doc_contents[:-1]]
        doc_texts = [filename.split("~~~~~filename~~~~~")[1] for filename in doc_contents[:-1]]

        return file_names, doc_texts
