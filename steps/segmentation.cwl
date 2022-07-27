cwlVersion: v1.1
class: CommandLineTool
label: segments each image in the directory for FTUs

requirements:
  DockerRequirement:
    dockerPull: hubmap/pas-ftu-segmentation
  DockerGpuRequirement: {}

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
  png_files:
    type: File[]
    outputBinding:
      glob: "*.png"
    doc: segmentation masks in png form

  json_files:
    type: File[]
    outputBinding:
      glob: "*.json"
    doc: segmentation masks in geoJSON format