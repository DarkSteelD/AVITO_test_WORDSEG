#!/bin/bash
eval "$(mamba shell hook --shell bash)"
mamba activate notebook
jupyter notebook
