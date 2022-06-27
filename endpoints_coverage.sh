#! /bin/bash

# This script prints a diff between endpoints in the official API docs
# and the ones that are implemented here.

rm -f endpoints.txt supported.txt

grep -Eo "['\"][^/][^'\":]+/[^'\" ]+['\"]" bigbuy/api.py \
  | grep -v application/json \
  | sed 's%{[^}]*}%{placeholder}%' \
  | sed -E "s%['\"]%%g" \
  | sort \
  >| supported.txt

curl -s https://api.bigbuy.eu/rest/doc/ \
  | grep 'swagger-data'|grep -o '\{.*\}' \
  | jq -r '.spec.paths|to_entries[].key' \
  | sed 's%/rest/%%' \
  | sed "s%\.{format}%%" \
  | sed 's%{[^}]*}%{placeholder}%' \
  | sort \
  >| endpoints.txt

git diff --no-index endpoints.txt supported.txt
rm -f endpoints.txt supported.txt