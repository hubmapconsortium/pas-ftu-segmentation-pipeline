#!/usr/bin/env cwl-runner

class: Workflow
cwlVersion: v1.0
label: Pipeline for performing FTU segmentation on PAS data

inputs:

  enable_manhole:
    label: "Whether to enable remote debugging via 'manhole'"
    type: boolean?

  data_directory:
    label: "Path to directory containing raw PAS dataset"
    type: Directory


outputs:

  png_files:
    outputSource: segmentation/png_files
    type: File[]
  json_files:
    outputSource: segmentation/json_files
    type: File[]

steps:

  - id: annotate-concatenate
    in:
      - id: data_directory
        source: data_directory
      - id: enable_manhole
        source: enable_manhole

    out:
      - png_files
      - json_files

    run: steps/segmentation.cwl
    label: "Performs FTU segmentation on PAS data"
