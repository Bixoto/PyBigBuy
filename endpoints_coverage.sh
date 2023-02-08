#! /bin/bash

# This script prints a diff between endpoints in the official API docs
# and the ones that are implemented here.

rm -f endpoints.txt supported.txt

# Grep everything that looks like an endpoint
# Exclude 'module/platforms' (the route is not documented) and the false positives 'application/…' and '/rest/order/…'
grep -Eo "['\"][^/][^'\":]+/[^'\" ]+['\"]" bigbuy/api.py \
  | grep -v application/json \
  | grep -v application/pdf \
  | sed 's%{[^}]*}%{placeholder}%' \
  | sed -E "s%['\"]%%g" \
  | grep -v '^module/platforms$' \
  | grep -v '\\\\/order\\\\/12[34]' \
  | sort \
  >| supported.txt

# Do the same using the BigBuy doc
curl -s http://api.bigbuy.eu/rest/doc.json \
  | jq -r '.paths|to_entries[].key' \
  | sed 's%/rest/%%' \
  | sed "s%\.{format}%%" \
  | sed 's%{[^}]*}%{placeholder}%' \
  | sort \
  >| endpoints.txt

git diff --no-index endpoints.txt supported.txt
rm -f endpoints.txt supported.txt
