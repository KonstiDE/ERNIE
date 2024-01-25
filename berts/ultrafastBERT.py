from transformers import AutoModelForMaskedLM, AutoTokenizer

from berts.helper.bert_helper import read_text


def analyse(preprocessed_file):
    print("Reading text...")
    cleaned_texts = read_text(preprocessed_file)

    model = AutoModelForMaskedLM.from_pretrained("pbelcak/UltraFastBERT-1x11-long")

    output = model.fit_transform(cleaned_texts)
