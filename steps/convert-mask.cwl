cwlVersion: v1.1
class: CommandLineTool
label: converts ometif files to tsv mask

requirements:
  DockerRequirement:
    dockerPull: hubmap/pas-ftu-segmentation
  DockerGpuRequirement: {}

baseCommand: /opt/v1/convert_mask.py

inputs:
  ome_tiff_files:
    type: File[]
    inputBinding:
      position: 0

outputs:
  tsv_file:
    type: File
    outputBinding:
      glob: "*.tsv"
    doc: tsv file of mask
  ome_tiff_files:
    type: File[]
    outputBinding:
      glob: "*.ome.tiff"