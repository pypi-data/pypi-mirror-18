#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

mkdir $DIR/demographer/data/
mkdir $DIR/temp_data
pushd $DIR/temp_data
wget http://www.socialsecurity.gov/OACT/babynames/names.zip
unzip names.zip
rm names.zip
popd
echo 'Building name dictionaries'
python -m demographer.cli.create_census_gender --census-data-path $DIR/temp_data/ --output $DIR/demographer/data/census_gender_dct.p
python -m demographer.cli.create_census_age --census-data-path $DIR/temp_data/ --output $DIR/demographer/data/census_age_dct.p
python -m demographer.cli.train_gender_classifier --output $DIR/demographer/data/gender_classifier.p
echo 'Data gathered and compiled, cleaning up files.'
rm -R $DIR/temp_data
echo 'Complete.'