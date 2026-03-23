from django.db import models


class SportCertificate(models.Model):
    """Model representing an athlete's sport medical certificate issued by an external doctor."""

    athlete = models.ForeignKey(
        "athletes.Athlete",
        on_delete=models.PROTECT,
        related_name="certificates",
        verbose_name="Atleta",
    )
    doctor = models.ForeignKey(
        "doctors.SportDoctor",
        on_delete=models.PROTECT,
        related_name="certificates",
        verbose_name="Medico Sportivo",
    )
    issue_date = models.DateField(verbose_name="Data Emissione")
    expiration_date = models.DateField(verbose_name="Data Scadenza")
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certificazione Medico-Sportiva"
        verbose_name_plural = "Certificazioni Medico-Sportive"
        ordering = ["-expiration_date", "athlete"]

    def __str__(self) -> str:
        return f"{self.athlete} — scad. {self.expiration_date}"

    def __repr__(self) -> str:
        return (
            f"SportCertificate(athlete_id={self.athlete_id}, "
            f"issue_date={self.issue_date!r}, expiration_date={self.expiration_date!r})"
        )
