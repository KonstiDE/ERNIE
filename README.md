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
The input of the ERNIE pipeline only consists of the previous mentioned config folder `gdelt_src` where all gdelt `.csv` files are stored. For fetching and downloading the data, ERNIE provides the the following function: `build_docs`:

| Argument  | Description                   | Default Value  |
|-----------|-------------------------------|----------------|
| fetching_chunk_size   | Parallelizes the fetching<br> (8, 16, 32 recommended)       | 16  |

Fetched data will be written to a file `.pkl` file via [Pickle](https://docs.python.org/3/library/pickle.html) and saved to `gdelt_out` directory. Each file represents one article fetched and can be traced back via the filename and the also in the name included line from the original `.csv` file. In case you want to look inside of the file yourself, load it with pickle (`pkl.load()`) and internally declare it as an instance of the `document.Document()` object. The following table describes the `Document` object and its attributes in detail:

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
---

### Data preprocessing
Although we extracted the real content out of the article in the previous step, still, preprocessing is nessecarry in order to feed out topic model clean data. Herefore, ERNIE provides a fully customizable function for cleaning the documents. Again, open the `main.py` file and execute the `preprocess_docs()`. The following arguments can be passed to the function in order to skip or execute certain steps of the pre-processing:

| Argument  | Description                   | Default Value  | Ignored if [...]
|-----------|-------------------------------|----------------| ----------------------------- |
| chunk_size | Size of a chunk that will be cleaned at once | 10.000 | - |
| duplicates | Whether **duplicates** are sorted out at the start | True | - |
| emojis | Whether **emojis** are removed | False | - |
| urls | Whether **urls** are removed | True | - |
| hashtags | Whether a **hashtag** itself is removed (#Obama -> Obama) | True | - |
| hashtags_content | Whether the content of the hashtag is removed (#Obama -> *\*Empty\**) | True | `hashtags=False` |
| ats | Whether an **@** itself is removed (@Trump -> Trump) | True | - |
| ats_content | Whether the content of the hashtag is removed (@Trump -> *\*Empty\**) | True | `ats=False` |
| punctuation | Whether characters of **, . ; ? !** are removed | True | - |
| digits | Whether **digits** are removed | False | - |
| stopwords | Whether **stopwords** are removed | True | - |
| stopwords_lang_codes | List of language codes from `stopwordsiso` (expl: `["en", "de", "es"]`) | `list()` | - |
| stopwords_custom | List of **custom stopwords that should be removed** | None | - |
| min_doc_length | Minimal **length of a document** worthy to include after preprocessing has been applied | 5 | - |
| duplicate_cleanup | Whether **duplicates** again are sorted out at the end | True | - |


