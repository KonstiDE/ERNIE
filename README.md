 # ⛩️ ERNIE ⛩️ <img src="assets/ernie.png" align="right" width="120" />
 
Welcome to the ERNIE repository. This repository will serve as a layer of presenting
my status on my internship in Sendai, (Japan 🏯), and deals with topic modeling pipelines and 
global media.

With a GDELT dataset, we try to analyse the interface of japanese media and internal crisis / event data to the 
international communities point of view.

Cheers, Caipi.


## Installation
To install the ERNIE repository and use the pipeline to model (GDELT) topics with it, clone this repository to your 
desired location. Make sure that you have enough storage space available (~1GB per 10.000 article sources).\

The ERNIE pipeline requires you only to edit two files to set up your BERT-Analysis. First, find
the ``config.py`` file under the `config` directory inside the root path of ERNIE and edit the cfg map in it.
The arguments explain as follows:

| Key       | Usage                                                              |
|-----------|--------------------------------------------------------------------|
| base_path | Main project directory: ``.../PyCharmProjects/ERNIE/``             |
| gdelt_src | Path to the src of the GDELT csv files: ``.../gdelt/``             |
| gdelt_out | Path that can be used to store data while processing: ``.../out/`` |

## Detailed explanation of different steps


