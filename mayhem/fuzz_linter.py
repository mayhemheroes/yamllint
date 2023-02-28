#! /usr/bin/env python3
import atheris
import sys
import random


import fuzz_helpers

with atheris.instrument_imports(include=["yamllint"]):
    from yamllint.config import YamlLintConfig
    from yamllint.linter import run

# Exceptions
from yaml.reader import ReaderError


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    conf = YamlLintConfig('extends: default')
    try:
        list(run(fdp.ConsumeRemainingString(), conf))
    except ReaderError:
        return -1
    except TypeError:
        if random.random() > 0.99:
            raise
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
