#! /bin/bash

cd intent_classifier
rasa train --out ../models/ --fixed-model-name intent_model nlu