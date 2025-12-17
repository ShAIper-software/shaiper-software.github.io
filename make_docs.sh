#!/bin/bash

. $ai_for_surrogate_modelling_path/bin/activate

rsync -av --progress  submodules/ai-for-surrogate-modelling/docs/docs . --exclude='scripts'

# mkdocs new docs
mkdocs build -f mkdocs-pdf.yml --verbose

mkdocs build --verbose

mkdocs serve

