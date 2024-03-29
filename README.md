 # ⛩️ ERNIE ⛩️ <img src="assets/ernie.png" align="right" width="120" />
 
Welcome to the ERNIE repository. This repository will serve as a layer of presenting
my status on my internship in Sendai, (Japan 🏯), and deals with topic modeling pipelines and 
global media.

With a GDELT dataset, we try to analyse the interface of japanese media and internal crisis / event data to the 
international communities point of view.

Cheers, Caipi.


## Installation
To install the ERNIE repository and use the pipeline to model (GDELT) topics with it, clone this repository to your 
desired location. Make sure that you have enough storage space available (~1GB per 5.000 article sources).

The ERNIE pipeline requires you only to edit two files to set up your BERT-Analysis. First, find
the ``config.py`` file under the `config` directory inside the root path of ERNIE and edit the cfg map in it.
The arguments explain as follows:

| Key       | Usage                                                               |
|-----------|---------------------------------------------------------------------|
| base_path | Main project directory: ``.../PyCharmProjects/ERNIE/``              |
| gdelt_src | Path to the src of the GDELT csv files: ``data/gdelt/``             |
| gdelt_out | Path that can be used to store data while processing: ``data/out/`` |


## Execution and Details

The ERNIE pipeline is build in minimalistic way when it comes to execution. Open up the ``main.py`` file in the root directory. Only a
few methods are needed to start a full analysis. Hereby, the we split the pipeline into smaller steps.

---
### Data aquisition
The input of the ERNIE pipeline only consists of the previous mentioned config folder `gdelt_src` where all gdelt `.csv` files are stored. For fetching and downloading the data, ERNIE provides the the following function: `build_docs()`:

| Argument  | Description                   | Default Value  |
|-----------|-------------------------------|----------------|
| fetching_chunk_size   | Parallelizes the fetching<br> (8, 16, 32 recommended)       | 16  |
| global_knowledge_graph_format   | `boolean` if the gkg format is underlying         | `False`  |

Fetched data will be written to a file `.pkl` file via [Pickle](https://docs.python.org/3/library/pickle.html) and saved to `gdelt_out` directory. Each file represents one article fetched and can be traced back via the filename and the also in the name included line from the original `.csv` file. In case you want to look inside of the file yourself, load it with pickle (`pkl.load()`) and internally declare it as an instance of the `document.Document()` object. The following table describes the **default** `Document` object and its attributes in detail:

| Attribute                  | Description
| -------------------------- | -------------------------------------------------------------------------------- |
| self.location              | Articles source (`str`)                                                          |
| self.location_result_count | -                                                                                |
| self.long                  | Longitude                                                                        |
| self.lat                   | Latitude                                                                         |
| self.url                   | Url pointing to the article                                                      |
| self.img_url               | Url of the main image from the articles page (if there is)                       |
| self.title                 | Title of the article                                                             |
| self.src_file              | GDELTs `.csv` source file                                                        |
| self.src_line              | Line within the GDELT `.csv` source file                                         |
| ——————————— | ———————————————————————————————————— |
| self.main_content          | Main content without HTML (might not be available depending on the urls status)  |
| self.html_content          | Raw HTML content                                                                 |
| self.cleaned_content       | Main content after preprocessing has been applied, else `None`                   |
| self.topic_information     | Topic information (`map`) after modeling has been applied, else `None`           |

If you set the fetching option `global_knowledge_graph_format` to True, the Document will have different arguments:

| Attribute                  | Description
| -------------------------- | -------------------------------------------------------------------------------- |
| self.date                  | Articles publication date, local time (`YYYYmmddHHMMss`)                         |
| self.source_name           | Name of the source form where the article was taken                              |
| self.url                   | Complete URL                                                                     |
| self.translationInfo       | Information about possible translation to english (optional)                     |
| self.counts                | GDELT pre-analysis of important counts (optional)                                |
| self.locations             | GDELT pre-analysis of the **exact** location of the event (optional)             |
| self.themes                | GDELT pre-analysis of the topic that the article is about (optional)             |
| self.tone                  | GDELT pre-analysis of the tone that the article was written in (optional)        |
| self.amounts               | GDELT pre-analysis of important numbers and digits                               |
| ——————————— | ———————————————————————————————————— |
| self.src_line              | GDELTs `.json` source file                                                       |
| self.src_file              | Line within the GDELT `.json` source file                                        |
| ——————————— | ———————————————————————————————————— |
| self.main_content          | Main content without HTML (might not be available depending on the urls status)  |
| self.html_content          | Raw HTML content                                                                 |
| self.cleaned_content       | Main content after preprocessing has been applied, else `None`                   |
| self.topic_information     | Topic information (`map`) after modeling has been applied, else `None`           |

---

### Data preprocessing

Although we extracted the real content out of the article in the previous step, still, preprocessing is nessecarry in order to feed out topic model clean data. Herefore, ERNIE provides a fully customizable function for cleaning the documents. Again, open the `main.py` file and execute the `preprocess_docs()`. The following arguments can be passed to the function in order to skip or execute certain steps of the pre-processing:

| Argument  | Description                   | Default Value  | Ignored if [...]              |
|-----------|-------------------------------|----------------| ----------------------------- |
| chunk_size | Size of a chunk that will be cleaned at once | 10.000 | - |
| duplicates | Whether **duplicates** are sorted out at the start | `True` | - |
| emojis | Whether **emojis** are removed | `False` | - |
| urls | Whether **urls** are removed | `True` | - |
| hashtags | Whether a **hashtag** itself is removed (#Obama -> Obama) | `True` | - |
| hashtags_content | Whether the content of the hashtag is removed (#Obama -> *\*Empty\**) | `True` | `hashtags=False` |
| ats | Whether an **@** itself is removed (@Trump -> Trump) | `True` | - |
| ats_content | Whether the content of the hashtag is removed (@Trump -> *\*Empty\**) | `True` | `ats=False` |
| punctuation | Whether characters of **, . ; ? !** are removed | `True` | - |
| digits | Whether **digits** are removed | `False` | - |
| stopwords | Whether **stopwords** are removed | `True` | - |
| stopwords_lang_codes | List of language codes from `stopwordsiso` (expl: `["en", "de", "es"]`) | `["en"]` | - |
| stopwords_custom | List of **custom stopwords that should be removed** | `list()` | - |
| min_doc_length | Minimal **length of a document** worthy to include after preprocessing has been applied | 5 | - |
| duplicate_cleanup | Whether **duplicates** again are sorted out at the end | `True` | - |

After preprocessing your documents, you will find your document files containing a now completed field `cleaned_text` with the cleaned document text. Note that only there will be `cleaned_text` if `main_content` was available (if the url was not corrupt). The cleaned text can be overwritten if you change arguments of the `preprocess_docs()` method and rerun it. In order to avoid mistakes, ERNIE will then ask you if you want to overwrite the already cleaned texts in the documents.

---

### Topic Modeling

To execute and fit the fetched, pre-processed documents into a BERTopic model, call `analyse_docs()`. Again, the attributes of this mehtods are explained in detail in the following:

| Argument   | Description                   | Default Value  | Ignored if [...]              |
|------------|-------------------------------|----------------| ----------------------------- |
| BERT_key   | Pretrained model from the Huggingface database (fresh model if `None`) | `None` | - |
| river_app  | Whether a [river approach](https://maartengr.github.io/BERTopic/getting_started/online/online.html) should be used | False | `BERT_key!=None` |
| river_conf | A map for the configuration of river, at the moment only supports:<br>`{chunk_size: 10.000}` | `river_app=False` |

Note that a ***river*** approach does not support every clusterin algorithm of BERTopic. You might for example not use clustering algorithms like `KMeansMiniBatch()` from [scikit-learn](https://scikit-learn.org/stable/) if using construction a river with `river_app=True`. Additionally, `analyse_docs()` inherits all arguments of the `betrtopic.BERTopic()` object to directly configure BERT inside ths function provided by ERNIE.

---

### Topic Labeling

Once your documents have been fitted to your desired model, call `label_topics()`. This method walks through every topic-keyword created by BERT and lets you pick an appropriate name for the whole topic. Since this algorithm requires the actual judge of a human, ERNIE will prompt you with generated keywords by the model and you can type in the name of your desired topic. Topics with the same topic name, will be merged automatically. If you cannot create a significant label for some keywords, mark the topic as `spam` to point out its an outlier and should not be used any further. Here, we still recommend to do this process twice, as merging and changing topics can only be done by repeating the entire process. Hopefully, we will provide a script for doing this in a more convenient fashion in the future. Once finished, a `custom_topics.pkl` file will be created serving as a dictionary between the topic-index of BERT and your labels.

### Topic matching

Once you are fine with your topic-labels you created execute `match_topics_from_model()`. This will translate BERTs indices of topics to your labels and apply it to the original documents. Note that this process is of course reversable by just calling `analyse_docs()` again to get back you topic indices or to apply a different set of topics.

