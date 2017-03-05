#!/bin/bash
#
# Randomly crawl things.
# Pass any argument to the script to use torify.
#

use_torify=$1
url='http://m.imdb.com'
random_id=$(python -c 'import random; print("{:07}".format(random.randrange(1, 9999999)))')
random_type=$(python -c 'import random; print(random.choice(("title", "name")))')

if [ $random_type == 'title' ]
then
    random_type_alias='tt'
else
    random_type_alias='nm'
fi

final_url="${url}/${random_type}/${random_type_alias}${random_id}"
echo "Indexing random ${random_type}: ${random_type_alias}${random_id}"

if [ $use_torify ]
then
    torify python imdbooo.py index -u $final_url
else
    python imdbooo.py index -u $final_url
fi
