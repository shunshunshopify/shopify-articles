#!/usr/bin/env bash

set -euo pipefail

source_file="${1:-drafts/shopify-development-companies-source-data.md}"

check_partner() {
  local number="$1"
  local company="$2"
  local url="$3"
  local html
  local raw_tier
  local display_status

  html="$(curl -sL --max-time 30 --retry 2 --retry-delay 1 "$url")"
  raw_tier="$(printf '%s' "$html" | rg -o -m 1 'tier_(registered|select|plus|premier|platinum)' || true)"

  case "$raw_tier" in
    tier_registered) display_status="Service Partner" ;;
    tier_select) display_status="Select" ;;
    tier_plus) display_status="Plus" ;;
    tier_premier) display_status="Premier" ;;
    tier_platinum) display_status="Platinum" ;;
    *) display_status="確認できず" ;;
  esac

  printf '%s\t%s\t%s\t%s\t%s\n' "$number" "$company" "$url" "${raw_tier:-not_found}" "$display_status"
}

export -f check_partner

perl -ne '
  if (/^## ([0-9]+)\. (.+)$/) {
    $number = $1;
    $company = $2;
  }
  if (/^- Shopify Partner Directory: (https:\/\/\S+)/) {
    print "$number\0$company\0$1\0";
  }
' "$source_file" \
  | xargs -0 -n 3 -P 8 bash -c 'check_partner "$@"' _ \
  | sort -t $'\t' -k1,1n
