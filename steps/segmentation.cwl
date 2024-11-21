cwlVersion: v1.1
class: CommandLineTool
label: segments each image in the directory for FTUs

requirements:
  DockerRequirement:
    dockerPull: hubmap/pas-ftu-segmentation:1.2.0
  DockerGpuRequirement: {}

baseCommand: /opt/v1/inference.py

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

  tissue_type:
    label: "Two letter code indicating organ sample is derived from"
    type: string
    inputBinding:
      position: 2


outputs:
  ome_tiff_files:
    type: File[]
    outputBinding:
      glob: "*.ome.tif"
    doc: binary segmentation masks in ome tiff form

  json_files:
    type: File[]
    outputBinding:
      glob: "*.json"
    doc: indexed segmentation masks in geoJSON format
