#!/bin/bash

#Script pour obtenir les logiciels necessaires au bon fonctionnement du pipeline variants
#ou les mettre? /usr/bin pour server: /scratch/bin ??


apt-get install git
apt-get install bio-perl
#workFolder=$(readlink -f $(dirname $0))
myPath=$(readlink -f $(dirname $0))
#myPath=~/Documents/Variants/Pipeline_NGS_Variants/Logiciels/

############    Telecharger tabix, l'extraire, le compiler, et creation du chemin #####################

echo "installation tabix"
cd $myPath
wget -c https://sourceforge.net/projects/samtools/files/tabix/tabix-0.2.6.tar.bz2
tar xvjf tabix-0.2.6.tar.bz2 ; rm tabix-0.2.6.tar.bz2 

cd $myPath/tabix-0.2.6/ ; make ; cd  $myPath
export PATH=$PATH:$myPath/tabix-0.2.6
cd $myPath
echo "tabix installe"
#fi

##########    Telecharger DBI,extraitre, etc ################
echo "installation DBI"
wget -c http://www.cpan.org/authors/id/T/TI/TIMB/DBI-1.634.tar.gz
tar zxvf DBI-1.634.tar.gz ; rm DBI-1.634.tar.gz

cd $myPath/DBI-1.634/ ; perl Makefile.PL; make ; make install ; cd $myPath
echo "DBI installe"

###########  Meme chose pour MySQL #########################
echo "installation MySQL"
wget -c http://search.cpan.org/CPAN/authors/id/M/MI/MICHIELB/DBD-mysql-4.033_02.tar.gz
tar zxvf DBD-mysql-4.033_02.tar.gz ; rm DBD-mysql-4.033_02.tar.gz
apt-get install libmysqlclient-dev
cd $myPath/DBD-mysql-4.033_02/ ; perl Makefile.PL; make ; make install ; cd $myPath
echo "MySQL installe"

################   Bio-perl ##############################
wget -c http://search.cpan.org/CPAN/authors/id/C/CJ/CJFIELDS/BioPerl-1.6.924.tar.gz
tar zxvf BioPerl-1.6.924.tar.gz ; rm BioPerl-1.6.924.tar.gz
cd $myPath/ /BioPerl-1.6.924/ ;perl Build.PL;

#TODO problem autorisation
./Build install
cd $myPath


###install Module::Build  ####
echo "#########################################################"
echo "#########################################################"
echo "Dans cpan Ecrire:"
echo "install Module::Build"
echo "exit"
echo "#########################################################"
echo "#########################################################"
cpan
#cpan install Module::Build


#################   Bio-DB-HTS  #######################
wget -c http://search.cpan.org/CPAN/authors/id/R/RI/RISHIDEV/Bio-DB-HTS-1.12.tar.gz
tar zxvf Bio-DB-HTS-1.12.tar.gz ; rm Bio-DB-HTS-1.12.tar.gz
cd $myPath/Bio-DB-HTS-1.12/ ; perl INSTALL.pl ; make install ;cd $myPath
cd $myPath/../System/Ensembl/ensembl-tools-release-84/scripts/variant_effect_predictor ;  perl INSTALL.pl 


# prendre fichier 43 45
# prendre fichier fasta humain (numero 27)
