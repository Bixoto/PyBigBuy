#! /bin/bash

# This script prints a diff between endpoints in the official API docs
# and the ones that are implemented here.

rm -f endpoints.txt supported.txt

# Grep everything that looks like an endpoint
# Exclude the false positives 'application/…' and '/rest/order/…'
grep -Eo "['\"][^/][^'\":]+/[^'\" ]+['\"]" bigbuy/api.py \
  | grep -v application/json \
  | grep -v application/pdf \
  | sed 's%{[^}]*}%{placeholder}%' \
  | sed -E "s%['\"]%%g" \
  | grep -v '\\\\/order\\\\/12[34]' \
  | sort \
  >| supported.txt

# Do the same using the BigBuy doc
# Exclude the category/categories routes, as they are deprecated
curl -s http://api.bigbuy.eu/rest/doc.json \
  | jq -r '.paths|to_entries[].key' \
  | sed 's%/rest/%%' \
  | sed "s%\.{format}%%" \
  | sed 's%{[^}]*}%{placeholder}%' \
  | grep -v 'catalog/categor' \
  | sort \
  >| endpoints.txt

git diff --no-index endpoints.txt supported.txt
ok="$?"
rm -f endpoints.txt supported.txt
if [ "$ok" = "1" ]; then
  exit 1
fi
