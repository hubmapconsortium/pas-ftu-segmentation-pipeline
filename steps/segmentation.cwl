cwlVersion: v1.0
class: CommandLineTool
label: segments each image in the directory for FTUs

hints:
  DockerRequirement:
    dockerPull: hubmap/pas-ftu-segmentation
baseCommand: /opt/inference.py

inputs:
  enable_manhole:
    label: "Whether to enable remote debugging via 'manhole'"
    type: boolean?
    inputBinding:
      position: 0

  data_directory:
    type: Directory
    doc: Path to processed dataset directory
    inputBinding:
      position: 1

outputs:
  png_masks:
    type: File[]
    outputBinding:
      glob: "*.png"
    doc: segmentation masks in png form

  json_masks:
    type: File[]
    outputBinding:
      glob: "*.json"
    doc: segmentation masks in geoJSON format