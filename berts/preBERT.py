from berts.helper.bert_helper import read_text


def analyse(preprocessed_file):
    print("Reading text...")
    file_names, cleaned_texts = read_text(preprocessed_file)





def pre_bert():
    analyse("preprocessed.txt")
