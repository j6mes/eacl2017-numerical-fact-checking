# Numerical Fact Checking
This repository contains a set of tools to rank a table's suitability for providing the information to fact-check a natural language utterance


## Environment
Will run locally on python3 or on SGE with anaconda3-2.5.0.
 * To run the table ranking algorithm, `numpy` and `scikit-learn` are required.
 * To run the corenlp NER extensions, `gradle` and `cython` `pyjnius` are required

    ```brew install gradle
    pip3 install --user numpy scikit-learn cython==0.24
    ```

    Alternatively, one can install gradle by:

    ```curl -s https://get.sdkman.io | bash
    sdk install gradle 3.1
    ```
    and if cython using anaconda:

    ```
    conda install -c anaconda cython=0.24
    ```

Installing jnius for python3 is non-trival, but is possible if cython==0.24 is installed. it may fail for any other version

    cd /tmp
    git clone https://github.com/kivy/pyjnius
    cd pyjnius
    sudo python3 setup.py -v install

Test

    $ python3
    >>> import jnius

If no error, then it's ok. If you get the following error:

    Traceback (most recent call last):
       File "<stdin>", line 1, in <module>
       File "/Users/james/anaconda/lib/python3.5/site-packages/jnius-1.1.dev0-py3.5-macosx-10.6-x86_64.egg/jnius/__init__.py", line 42, in <module>
        if "ANDROID_ARGUMENT" in os.environ:
    NameError: name 'os' is not defined

Then edit the offending file and delete the whole block of code under the android argument.




## Set Up
Data must be downloaded from Pasupat Panupong's site and extracted to the root directory. Run `setup.sh` in the scripts folder to do that on SGE or run the following commands (in the root of this git repo) if testing locally.

    wget http://nlp.stanford.edu/software/sempre/wikitable/WikiTableQuestions-1.0.2.zip
    unzip WikiTableQuestions-1.0.2.zip


## Run Table Ranking
To rank the tables,

    python3 data_reader.py [bow] [ngrams] [continuous features]

BOW:

    0 - rank using jaccard and cosine scores of header/utterance BOWs only
    1 - add intersection of bag of words to features
    2 - add union of bag of words to features
    3 - add both

NGrams:

    0 - rank using jaccard and cosine scores of character level trigrams
    1 - add intersection of trigrams to features
    2 - add union of trigrams to features
    3 - add both


Continous Features:

    Not yet implemented - ignore for now

Or, to run on SGE, run `submit.sh` from the `scripts` folder

## Run NER Scripts
CoreNLP 3.6 can be installed through the `gradle` script. This will download and install CoreNLP and generate the JAR classpath which is needed for `pyjnius` to work.

    gradle writeClasspath

Or try (if gradle daemon is not installed and is being run from the gitrepo)

    ./gradlew writeClasspath

This outputs the classpath to `build/classpath.txt`. This only needs to be done once.


Then use

    python3 corenlp.py

At the moment, the input utterance must be set in the file, this is very much work in progress!
