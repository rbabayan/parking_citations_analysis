#!/bin/bash

###########################
#    create sqlite db     #
###########################
echo
echo "Creating SQLite Database by importing csv dataset...";
echo "This may take a minute or two ( ͡° ͜ʖ ͡°)ﾉ⌐■-■";
sqlite3 ./dataset.db <<'END_SQL'
.mode csv
.import ./dataset.csv citations
END_SQL