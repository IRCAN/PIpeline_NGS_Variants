![Logo IRCAN](http://ircan.org/images/stories/logo_ircan.png)

# Pipeline_NGS_Variants Project

### By Ludovic Kosthowa (Intern Master student)
### During 6 month internship
### Created 15/02/2016

---
__INFORMATIONS :__

This project is not finished. I'm currently working on this project so all code could be changed.
Thank you for your understanding.

---

Workspace of created pipeline for variants NGS analysis:
	This pipeline is used to find and annotate variants from the Ion PGM.
	This pipeline runs on each analysis made with the PGM.

__Repository:__
- "__scripts__" repository contain all scripts

- "__Resultats__" repository contain output file created by scripts

- "__Data__" repository contain necessary data for running scripts.
If you download the repository for the first time, you need to download the  ["homo_sapiens_vep_84_GRCh37.tar.gz"](http://ftp.ensembl.org/pub/current_variation/VEP/") from ensembl website and ["CosmicCompleteExport.tsv"](http://cancer.sanger.ac.uk/cosmic/download) from Cosmic database. You must add this data respectively in Data/Ensembl and Data/Cosmic repository.

- "__Logiciels__" repository contain all softwares used by scripts
- "__Documents__" repository contain informations about pipeline like graph

__Run:__

To run analysis, enter this command:
```
python main.py --hot /path/to/list/listeHotspot.tsv --vcf Path/to/repertory/with_vcf_file/
S
```

