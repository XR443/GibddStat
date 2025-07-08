#!/bin/bash

declare -a years=(2022 2023 2024)

for year in "${years[@]}"
do
  python3 GibddStatParser.py --year $year
done
