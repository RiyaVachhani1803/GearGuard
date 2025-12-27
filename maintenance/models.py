from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    purchase_date = models.DateField()
    warranty_till = models.DateField()

    maintenance_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    is_scrapped = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MaintenanceRequest(models.Model):
    REQUEST_TYPE = [
        ("CORRECTIVE", "Corrective"),
        ("PREVENTIVE", "Preventive"),
    ]

    STATUS = [
        ("NEW", "New"),
        ("IN_PROGRESS", "In Progress"),
        ("REPAIRED", "Repaired"),
        ("SCRAP", "Scrap"),
    ]

    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE)
    status = models.CharField(max_length=20, choices=STATUS, default="NEW")

    scheduled_date = models.DateField(null=True, blank=True)
    duration_hours = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.equipment and not self.team:
            self.team = self.equipment.maintenance_team

        if self.status == "SCRAP":
            self.equipment.is_scrapped = True
            self.equipment.save()

        super().save(*args, **kwargs)
