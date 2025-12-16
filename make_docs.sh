#!/bin/bash

git submodule add https://code.it4i.cz/kra568/ai-surrogate-modelling submodules/ai-for-surrogate-modelling
git submodule update --init --recursive
git submodule update --remote

. $ai_for_surrogate_modelling_path/bin/activate

rsync -av --progress  submodules/ai-for-surrogate-modelling/docs/docs . --exclude='scripts'

# mkdocs new docs
mkdocs build -f mkdocs-pdf.yml --verbose

mkdocs build --verbose

mkdocs serve

