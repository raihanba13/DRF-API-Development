from django.db import models


class Territory(models.Model):
    name = models.CharField(max_length=48)
    code_2 = models.CharField(max_length=2)
    code_3 = models.CharField(max_length=3)
    local_currency = models.ForeignKey(
        "Currency", related_name="territories", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "territory"
        verbose_name = "territory"
        verbose_name_plural = "territories"
        ordering = ("name",)


class Currency(models.Model):
    name = models.CharField(max_length=48)
    symbol = models.CharField(max_length=4)
    code = models.CharField(max_length=3)

    class Meta:
        db_table = "currency"
        verbose_name = "currency"
        verbose_name_plural = "currencies"


class DSR(models.Model):
    class Meta:
        db_table = "dsr"

    STATUS_ALL = (
        ("failed", "FAILED"),
        ("ingested", "INGESTED"),
    )

    path = models.CharField(max_length=256)
    period_start = models.DateField(null=True)
    period_end = models.DateField(null=True)

    status = models.CharField(
        choices=STATUS_ALL, default=STATUS_ALL[0][0], max_length=48
    )

    territory = models.ForeignKey(
        Territory, related_name="dsrs", on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name="dsrs", on_delete=models.CASCADE
    )

class Resource(models.Model):
    # 30 is enough though
    dsp_id = models.CharField(max_length=40)
    title = models.CharField(max_length=40, null=True, blank=True)
    # 15 per person, max 10
    artists = models.CharField(max_length=150, null=True, blank=True)
    isrc = models.CharField(max_length=20, null=True, blank=True)
    usages = models.IntegerField(default=0, null=True, blank=True)
    revenue = models.FloatField(default=0, null=True, blank=True)
    # will join manually
    dsrs_id = models.IntegerField(default=0, null=True, blank=True)

    # dsrs = models.ForeignKey(
    #     DSR, related_name="dsr", on_delete=models.CASCADE, null=True
    # )


    class Meta:
        db_table = "resource"
        verbose_name = "resource"
        verbose_name_plural = "resources"
