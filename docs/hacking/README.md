# Hacking on `genderbias`

If you're reading this page, then welcome to the team!

## Tutorial: Writing a new Detector

In this tutorial, we'll write a new `Detector`. `Detector`s are the tools that this package uses to detect a bias in text.

Let's implement a detector that finds out if the text is calling somebody some type of amphibian. (This is obviously a toy example!)

### Setting up the submodule

First, let's create a new submodule inside the `genderbias` package. In a shell, run:

```
$ cd genderbias/
$ mkdir amphibian
$ touch amphibian/__init__.py
```

If you are unfamiliar with Python submodules and why we use the weird name `__init__.py`, check out [this Python documentation](https://docs.python.org/3/tutorial/modules.html).


### Creating a wordlist

Next, let's construct a word-list of words we want to flag. In a file named `wordlist.txt` in the `amphibian/` directory, write the following, each word on its own line:

```
frog
toad
tadpole
salamander
```

### Creating the detector

In `amphibian/__init__.py`, we'll _inherit_ from the base `Detector` class:

```python
from genderbias.detector import Detector, Flag, Issue, Report


class AmphibianDetector(Detector):

    def get_report(self, doc):
        pass
```

Let's include the wordlist as a variable named `AMPHIBIAN_WORDS`:

```python
from genderbias.detector import Detector, Flag, Issue, Report

AMPHIBIAN_WORDS = open(_dir + "/wordlist.txt", 'r').readlines()

class AmphibianDetector(Detector):

    def get_report(self, doc):
        pass
```

### Flagging amphibian-related words

We only have one function to implement: `get_report`. This function must accept a `Document` and return a `Report`.

Let's flag any time one of the words from our wordlist comes up (using the `Flag` class), and add these to the `Report`:

```python
from genderbias.detector import Detector, Flag, Issue, Report

AMPHIBIAN_WORDS = open(_dir + "/wordlist.txt", 'r').readlines()

class AmphibianDetector(Detector):

    def get_report(self, doc):
        amphibian_report = Report("Amphibians")
        words_with_indices = doc.words_with_indices()

        for word, start, stop in words_with_indices:
            if word.lower() in AMPHIBIAN_WORDS:
                amphibian_report.add_flag(
                    Flag(start, stop, Issue(
                        "AmphibianWord",
                        "You shouldn't call someone an amphibian. '{word}' is an amphibian-sounding word.".format(
                            word=word),
                        "Try replacing with phrasing that emphasizes that this person is a human."
                    ))
                )

        return amphibian_report

```

We can also, optionally, set a summary of our findings:

```python
from genderbias.detector import Detector, Flag, Issue, Report

AMPHIBIAN_WORDS = open(_dir + "/wordlist.txt", 'r').readlines()

class AmphibianDetector(Detector):

    def get_report(self, doc):
        amphibian_report = Report("Amphibians")
        words_with_indices = doc.words_with_indices()

        found_amphibian = False
        for word, start, stop in token_indices:
            if word.lower() in AMPHIBIAN_WORDS:
                found_amphibian = True
                amphibian_report.add_flag(
                    Flag(start, stop, Issue(
                        "AmphibianWord",
                        "You shouldn't call someone an amphibian. '{word}' is an amphibian-sounding word.".format(
                            word=word),
                        "Try replacing with phrasing that emphasizes that this person is a human."
                    ))
                )

        if found_amphibian:
            amphibian_report.set_summary("Found some amphibian words. These are highly recommended against being used.")

        return amphibian_report

```

### Using the `Detector` in the main package

All done! Assuming the new `Detector` is correctly located, it will be automatically located by the `genderbias` script.

You can check it is available using:
```shell
$ genderbias --list-detectors
...
AmphibianDetector
```
(where the `...` may be a list of other `Detector`s)

If it's listed using the above command, then we're done! Now, when users run `genderbias`, it will detect if they have called someone some sort of amphibian-sounding word:

```shell
$ genderbias --file my-letter.txt
Amphibians
 [50-54] AmphibianWord: You shouldn't call someone an amphibian. 'frog' is an amphibian-sounding word. Try replacing with phrasing that emphasizes that this person is a human.
 SUMMARY: Found some amphibian words. These are highly recommended against being used.
```
