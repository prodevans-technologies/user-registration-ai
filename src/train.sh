#!/usr/bin/env bash

# Activating the python environment
source  /Users/rajanikant/venv/flask/bin/activate

# Setting up the essential evn variables
IMAGE_SIZE=224
ARCHITECTURE="mobilenet_0.50_${IMAGE_SIZE}"

#------------------------------------------------------------------------
# Training the model
#------------------------------------------------------------------------
python -m scripts.retrain \
  --bottleneck_dir=train_meta/bottlenecks \
  --how_many_training_steps=500 \
  --model_dir=train_meta/models/ \
  --summaries_dir=train_meta/training_summaries/"${ARCHITECTURE}" \
  --output_graph=train_meta/retrained_graph.pb \capture_status
  --output_labels=train_meta/retrained_labels.txt \
  --architecture="${ARCHITECTURE}" \
  --image_dir=images

#------------------------------------------------------------------------
# very likely get improved results (i.e. higher accuracy) by training for longer
#------------------------------------------------------------------------
python -m scripts.retrain \
  --bottleneck_dir=train_meta/bottlenecks \
  --model_dir=train_meta/models/"${ARCHITECTURE}" \
  --summaries_dir=train_meta/training_summaries/"${ARCHITECTURE}" \
  --output_graph=train_meta/retrained_graph.pb \
  --output_labels=train_meta/retrained_labels.txt \
  --architecture="${ARCHITECTURE}" \
  --image_dir=images


#------------------------------------------------------------------------
# Testing the output
#------------------------------------------------------------------------
python -m scripts.label_image \
    --graph=train_meta/retrained_graph.pb  \
    --labels=train_meta/retrained_labels.txt \
    --image=images/amit/19.jpeg