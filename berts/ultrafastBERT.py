import bertopic

from bertopic import BERTopic

# import cramming

# possible data https://huggingface.co/datasets/olm/gdelt-news-headlines

# from transformers import AutoModelForMaskedLM, AutoTokenizer
#
# tokenizer = AutoTokenizer.from_pretrained("pbelcak/UltraFastBERT-1x11-long")
# model = AutoModelForMaskedLM.from_pretrained("pbelcak/UltraFastBERT-1x11-long")
#
# from datasets import load_dataset
#
# dataset = load_dataset("olm/gdelt-news-headlines")


def analyse(preprocessed_file, preBERT):
    pass
    # print("Reading text...")
    # # file_names, cleaned_texts = read_text(preprocessed_file)
    #
    # text = "Replace me by any text you'd like."
    # encoded_input = tokenizer(text, return_tensors='pt')
    # output = model(**encoded_input)
    #
    # print(output)


def analyse_bert(model_name):
    analyse("preprocessed.txt", model_name)


if __name__ == '__main__':
    analyse_bert("pbelcak/UltraFastBERT-1x11-long")
