"""Management command to import geography data from bundled CSV files.

Data sources:
- countries.csv: ISO 3166-1 alpha-3 country codes
- provinces.csv: Italian provinces (ISTAT)
- municipalities.csv: Italian municipalities (ISTAT)

See geography/data/README.md for source details.
"""

import csv
import logging
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from geography.models import Country, Municipality, Province

logger: logging.Logger = logging.getLogger(__name__)

DATA_DIR: Path = Path(__file__).resolve().parent.parent.parent / "data"


class Command(BaseCommand):
    help: str = "Import geography data (countries, provinces, municipalities) from bundled CSV files."

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--countries",
            action="store_true",
            help="Import only countries",
        )
        parser.add_argument(
            "--provinces",
            action="store_true",
            help="Import only provinces",
        )
        parser.add_argument(
            "--municipalities",
            action="store_true",
            help="Import only municipalities",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            dest="import_all",
            help="Import all datasets (default if no flag given)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and validate data without writing to DB",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        dry_run: bool = options["dry_run"]
        import_countries: bool = options["countries"]
        import_provinces: bool = options["provinces"]
        import_municipalities: bool = options["municipalities"]
        import_all: bool = options["import_all"]

        # Default to all if no specific flag given
        if not any([import_countries, import_provinces, import_municipalities, import_all]):
            import_all = True

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN — no data will be written."))

        has_errors: bool = False

        if import_all or import_countries:
            self._import_countries(dry_run)
        if import_all or import_provinces:
            self._import_provinces(dry_run)
        if import_all or import_municipalities:
            success: bool = self._import_municipalities(dry_run)
            if not success:
                has_errors = True

        if has_errors:
            self.stdout.write(self.style.WARNING("Import completed with errors."))
        else:
            self.stdout.write(self.style.SUCCESS("Import completed."))

    def _read_csv(self, filename: str) -> list[dict[str, str]]:
        """Read a CSV file from the data directory."""
        filepath: Path = DATA_DIR / filename
        if not filepath.exists():
            raise CommandError(f"CSV file not found: {filepath}")
        with open(filepath, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _import_countries(self, dry_run: bool) -> None:
        """Import countries from countries.csv."""
        rows: list[dict[str, str]] = self._read_csv("countries.csv")
        created: int = 0
        updated: int = 0
        skipped: int = 0

        for row in rows:
            iso_code: str = row.get("iso_code", "").strip()
            name: str = row.get("name", "").strip()
            if not iso_code or not name:
                skipped += 1
                logger.warning("Skipping country row with missing data: %s", row)
                continue
            if not dry_run:
                _, was_created = Country.objects.update_or_create(
                    iso_code=iso_code,
                    defaults={"name": name, "is_active": True},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        if dry_run:
            self._report("Countries", len(rows) - skipped, 0, skipped, dry_run=True)
            return

        self._report("Countries", created, updated, skipped)

    def _import_provinces(self, dry_run: bool) -> None:
        """Import provinces from provinces.csv."""
        rows: list[dict[str, str]] = self._read_csv("provinces.csv")
        created: int = 0
        updated: int = 0
        skipped: int = 0

        for row in rows:
            code: str = row.get("code", "").strip()
            name: str = row.get("name", "").strip()
            if not code or not name:
                skipped += 1
                logger.warning("Skipping province row with missing data: %s", row)
                continue
            if not dry_run:
                _, was_created = Province.objects.update_or_create(
                    code=code,
                    defaults={"name": name},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        if dry_run:
            self._report("Provinces", len(rows) - skipped, 0, skipped, dry_run=True)
            return

        self._report("Provinces", created, updated, skipped)

    def _import_municipalities(self, dry_run: bool) -> bool:
        """Import municipalities from municipalities.csv. Returns True on success."""
        rows: list[dict[str, str]] = self._read_csv("municipalities.csv")
        created: int = 0
        skipped: int = 0

        # Build province lookup map
        province_map: dict[str, Province] = {
            p.code: p for p in Province.objects.all()
        }

        if not province_map:
            self.stdout.write(
                self.style.ERROR(
                    "No provinces in DB. Import provinces first (--provinces or --all)."
                )
            )
            return False

        if dry_run:
            # Validate rows counting skipped rows (not unique codes)
            missing_codes: set[str] = set()
            for row in rows:
                name: str = row.get("name", "").strip()
                province_code: str = row.get("province_code", "").strip()
                if not name or not province_code or province_code not in province_map:
                    skipped += 1
                    if province_code and province_code not in province_map:
                        missing_codes.add(province_code)
            if missing_codes:
                self.stdout.write(
                    self.style.WARNING(
                        f"Unknown province codes in CSV: {sorted(missing_codes)}"
                    )
                )
            self._report("Municipalities", len(rows) - skipped, 0, skipped, dry_run=True)
            return True

        with transaction.atomic():
            for row in rows:
                name = row.get("name", "").strip()
                province_code = row.get("province_code", "").strip()
                if not name or not province_code:
                    skipped += 1
                    logger.warning("Skipping municipality row with missing data: %s", row)
                    continue
                province: Province | None = province_map.get(province_code)
                if province is None:
                    skipped += 1
                    logger.warning(
                        "Unknown province code '%s' for municipality '%s', skipping.",
                        province_code,
                        name,
                    )
                    continue
                _, was_created = Municipality.objects.get_or_create(
                    name=name,
                    province=province,
                )
                if was_created:
                    created += 1

        self._report("Municipalities", created, 0, skipped)
        return True

    def _report(
        self,
        entity: str,
        created: int,
        updated: int,
        skipped: int,
        dry_run: bool = False,
    ) -> None:
        """Report import statistics."""
        if dry_run:
            msg: str = f"{entity}: {created} rows parsed (dry run, no writes)."
            if skipped:
                msg += f" {skipped} would be skipped."
        else:
            msg = f"{entity}: {created} created, {updated} updated, {skipped} skipped."
        self.stdout.write(self.style.SUCCESS(msg))
        logger.info(msg)
