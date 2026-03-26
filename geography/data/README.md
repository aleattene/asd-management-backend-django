# Geography Data Sources

CSV files used by the `import_geography` management command.

## Sources

- **countries.csv**: ISO 3166-1 alpha-3 country codes.
  Source: ISO 3166-1 standard (https://www.iso.org/iso-3166-country-codes.html).
  Country names translated to Italian where available.

- **provinces.csv**: Italian provinces (sigle automobilistiche).
  Source: ISTAT — Elenco comuni italiani
  (https://www.istat.it/it/archivio/6789).

- **municipalities.csv**: Italian municipalities (comuni).
  Source: ISTAT — Elenco comuni italiani
  (https://www.istat.it/it/archivio/6789).

## Update procedure

1. Download the latest dataset from ISTAT
2. Regenerate the CSV files
3. Run `python manage.py import_geography`
