import os

from athletes.models import Category
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from payment_methods.models import PaymentMethod

from users.models import CustomUser, UserRole

PAYMENT_METHOD_NAMES: list[str] = ["Bonifico Bancario", "Contanti", "POS", "Assegno"]

CATEGORIES: list[dict] = [
    {"code": "U08", "description": "Under 8", "age_range": "6-8"},
    {"code": "U10", "description": "Under 10", "age_range": "9-10"},
    {"code": "U12", "description": "Under 12", "age_range": "11-12"},
    {"code": "U14", "description": "Under 14", "age_range": "13-14"},
    {"code": "U16", "description": "Under 16", "age_range": "15-16"},
    {"code": "U18", "description": "Under 18", "age_range": "17-18"},
    {"code": "SEN", "description": "Senior", "age_range": "18+"},
]


class Command(BaseCommand):
    """Populate the database with realistic development data."""

    help = (
        "Seed the database with development data. "
        "For safe repeat runs, use --flush to clear existing data first."
    )

    def add_arguments(self, parser) -> None:  # type: ignore[override]
        parser.add_argument(
            "--flush",
            action="store_true",
            help=(
                "Delete seeded data (users, athletes, enrollments, certificates, "
                "trainers, doctors, companies, payment methods, invoices, receipts) "
                "before seeding. Superusers and geography data are preserved. "
                "Required for safe repeat runs."
            ),
        )

    def handle(self, *args, **options) -> None:
        if not settings.DEBUG:
            raise CommandError(
                "seed_db is intended for development only and cannot run with DEBUG=False. "
                "Set DEBUG=True or use the correct settings module."
            )

        # Validate all required env vars upfront — before any DB write.
        self._validate_seed_env()

        try:
            from factories import (
                AthleteFactory,
                CompanyFactory,
                EnrollmentFactory,
                InvoiceFactory,
                ReceiptFactory,
                SportCertificateFactory,
                SportDoctorFactory,
                TrainerFactory,
                UserFactory,
            )
        except ModuleNotFoundError as exc:
            if exc.name and exc.name.split(".")[0] in {"factory", "faker", "factories"}:
                raise CommandError(
                    "Dev dependencies are not installed. "
                    "Run: pip install -r requirements_dev.txt, then retry."
                ) from exc
            raise

        self.AthleteFactory = AthleteFactory
        self.CompanyFactory = CompanyFactory
        self.EnrollmentFactory = EnrollmentFactory
        self.InvoiceFactory = InvoiceFactory
        self.ReceiptFactory = ReceiptFactory
        self.SportCertificateFactory = SportCertificateFactory
        self.SportDoctorFactory = SportDoctorFactory
        self.TrainerFactory = TrainerFactory
        self.UserFactory = UserFactory

        with transaction.atomic():
            if options["flush"]:
                self._flush()
            elif CustomUser.objects.filter(is_superuser=False).exists():
                raise CommandError(
                    "Database already contains seeded data. "
                    "Use --flush to clear existing data before re-seeding."
                )

            self.stdout.write("Seeding database...")

            payment_methods = self._seed_payment_methods()
            categories = self._seed_categories()
            users = self._seed_users()
            trainers = self._seed_trainers(users["trainers"])
            doctors = self._seed_doctors()
            athletes = self._seed_athletes(users["members"], categories, trainers)
            self._seed_enrollments(athletes)
            self._seed_certificates(athletes, doctors)
            companies = self._seed_companies()
            self._seed_invoices(companies, payment_methods)
            self._seed_receipts(users["members"] + users["trainers"], payment_methods)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_seed_env(self) -> None:
        """Raise CommandError if any required SEED_* env var is missing."""
        required: list[str] = [
            "SEED_SUPERADMIN_USERNAME",
            "SEED_SUPERADMIN_EMAIL",
            "SEED_SUPERADMIN_PASSWORD",
            "SEED_ADMIN_USERNAME",
            "SEED_ADMIN_EMAIL",
            "SEED_ADMIN_PASSWORD",
        ]
        missing: list[str] = [var for var in required if not os.environ.get(var)]
        if missing:
            raise CommandError(
                f"The following environment variables are required but not set: "
                f"{', '.join(missing)}"
            )

    def _flush(self) -> None:
        """Delete seeded data: all non-superuser users, athletes, enrollments,
        certificates, trainers, doctors, companies, payment methods, invoices,
        and receipts. Superusers, geography data, and auth groups/permissions
        are preserved."""
        from athletes.models import Athlete, Category
        from certificates.models import SportCertificate
        from companies.models import Company
        from doctors.models import SportDoctor
        from enrollments.models import Enrollment
        from invoices.models import Invoice
        from payment_methods.models import PaymentMethod
        from receipts.models import Receipt
        from staff.models import Trainer

        self.stdout.write("Flushing existing data...")
        Receipt.objects.all().delete()
        Invoice.objects.all().delete()
        SportCertificate.objects.all().delete()
        Enrollment.objects.all().delete()
        Athlete.objects.all().delete()
        Trainer.objects.all().delete()
        SportDoctor.objects.all().delete()
        Category.objects.all().delete()
        Company.objects.all().delete()
        PaymentMethod.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()
        self.stdout.write("Flush complete.")

    def _seed_payment_methods(self) -> list:
        methods = []
        for name in PAYMENT_METHOD_NAMES:
            pm, _ = PaymentMethod.objects.update_or_create(
                name=name, defaults={"is_active": True}
            )
            methods.append(pm)
        self.stdout.write(f"  Payment methods: {len(methods)}")
        return methods

    def _seed_categories(self) -> list:
        cats = []
        for data in CATEGORIES:
            cat, _ = Category.objects.update_or_create(
                code=data["code"],
                defaults={
                    "description": data["description"],
                    "age_range": data["age_range"],
                    "is_active": True,
                },
            )
            cats.append(cat)
        self.stdout.write(f"  Categories: {len(cats)}")
        return cats

    def _seed_users(self) -> dict:
        roles: list[dict] = [
            {"role": UserRole.ADMIN, "count": 2, "key": "admins"},
            {"role": UserRole.OPERATOR, "count": 3, "key": "operators"},
            {"role": UserRole.TRAINER, "count": 4, "key": "trainers"},
            {"role": UserRole.MEMBER, "count": 10, "key": "members"},
            {"role": UserRole.EXTERNAL, "count": 3, "key": "externals"},
        ]
        created: dict = {}
        for cfg in roles:
            users = [self.UserFactory(role=cfg["role"]) for _ in range(cfg["count"])]
            created[cfg["key"]] = users
            self.stdout.write(f"  Users ({cfg['role']}): {len(users)}")

        # Ensure one known superadmin
        superadmin_username: str = os.environ["SEED_SUPERADMIN_USERNAME"]
        superadmin_email: str = os.environ["SEED_SUPERADMIN_EMAIL"]
        superadmin_password: str = os.environ["SEED_SUPERADMIN_PASSWORD"]
        superadmin, _was_created = CustomUser.objects.update_or_create(
            username=superadmin_username,
            defaults={
                "email": superadmin_email,
                "role": UserRole.SUPERADMIN,
                "is_superuser": True,
                "is_staff": True,
            },
        )
        superadmin.set_password(superadmin_password)
        superadmin.save()
        self.stdout.write(
            f"  Superadmin {'created' if _was_created else 'updated'} (username: {superadmin_username})"
        )

        # Ensure one known admin
        admin_username: str = os.environ["SEED_ADMIN_USERNAME"]
        admin_email: str = os.environ["SEED_ADMIN_EMAIL"]
        admin_password: str = os.environ["SEED_ADMIN_PASSWORD"]
        admin, _was_created = CustomUser.objects.update_or_create(
            username=admin_username,
            defaults={"email": admin_email, "role": UserRole.ADMIN},
        )
        admin.set_password(admin_password)
        admin.save()
        self.stdout.write(
            f"  Admin {'created' if _was_created else 'updated'} (username: {admin_username})"
        )

        return created

    def _seed_trainers(self, trainer_users: list) -> list:
        trainers = [self.TrainerFactory(user=u) for u in trainer_users]
        self.stdout.write(f"  Trainers: {len(trainers)}")
        return trainers

    def _seed_doctors(self) -> list:
        doctors = [self.SportDoctorFactory() for _ in range(3)]
        self.stdout.write(f"  Sport doctors: {len(doctors)}")
        return doctors

    def _seed_athletes(self, guardians: list, categories: list, trainers: list) -> list:
        athletes = []
        for i, guardian in enumerate(guardians):
            category = categories[i % len(categories)]
            trainer = trainers[i % len(trainers)]
            athlete = self.AthleteFactory(
                guardian=guardian, category=category, trainer=trainer
            )
            athletes.append(athlete)
        # Add a few more athletes without trainer
        for i in range(5):
            athlete = self.AthleteFactory(
                guardian=guardians[i % len(guardians)],
                category=categories[i % len(categories)],
                trainer=None,
            )
            athletes.append(athlete)
        self.stdout.write(f"  Athletes: {len(athletes)}")
        return athletes

    def _seed_enrollments(self, athletes: list) -> None:
        count = 0
        for athlete in athletes:
            self.EnrollmentFactory(athlete=athlete, season="2025/2026")
            count += 1
        self.stdout.write(f"  Enrollments: {count}")

    def _seed_certificates(self, athletes: list, doctors: list) -> None:
        count = 0
        for i, athlete in enumerate(athletes[:15]):
            doctor = doctors[i % len(doctors)]
            self.SportCertificateFactory(athlete=athlete, doctor=doctor)
            count += 1
        self.stdout.write(f"  Certificates: {count}")

    def _seed_companies(self) -> list:
        companies = [self.CompanyFactory() for _ in range(10)]
        self.stdout.write(f"  Companies: {len(companies)}")
        return companies

    def _seed_invoices(self, companies: list, payment_methods: list) -> None:
        count = 0
        for i in range(20):
            self.InvoiceFactory(
                company=companies[i % len(companies)],
                payment_method=payment_methods[i % len(payment_methods)],
            )
            count += 1
        self.stdout.write(f"  Invoices: {count}")

    def _seed_receipts(self, users: list, payment_methods: list) -> None:
        count = 0
        for i in range(15):
            self.ReceiptFactory(
                user=users[i % len(users)],
                payment_method=payment_methods[i % len(payment_methods)],
            )
            count += 1
        self.stdout.write(f"  Receipts: {count}")
