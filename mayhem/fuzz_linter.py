#! /usr/bin/env python3
# Atheris fuzz harness for yamllint: lint fuzzer-generated YAML with the default
# config through yamllint.linter.run (the same code path as the original
# `fuzz-linter` target). Atheris instruments the yamllint package at import time,
# which is where coverage (edges) comes from.
import sys

import atheris

import fuzz_helpers

with atheris.instrument_imports(include=["yamllint"]):
    from yamllint.config import YamlLintConfig
    from yamllint.linter import run

# Exceptions
from yaml.reader import ReaderError

CONF = YamlLintConfig('extends: default')


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        list(run(fdp.ConsumeRemainingString(), CONF))
    except ReaderError:
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
