from django.db import models
from django.db.models import ForeignKey, DateTimeField, DecimalField, IntegerField, CharField, deletion
from djchoices import DjangoChoices, ChoiceItem
from rest_framework.compat import MinValueValidator

from dbaas.models import Server


# ====================================================================================
class Metrics_Cpu(models.Model):
    class Meta:
        db_table = 'metrics_cpu'

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    created_dttm = DateTimeField(editable=False, null=False)
    cpu_idle_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    cpu_user_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    cpu_system_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    cpu_iowait_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    cpu_irq_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    cpu_steal_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    cpu_guest_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    cpu_guest_nice_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    error_cnt = IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    error_msg = CharField(max_length=2000, null=False, default='')

class Metrics_MountPoint(models.Model):
    class Meta:
        db_table = 'metrics_mount_point'

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    created_dttm = DateTimeField(editable=False, null=False)
    mount_point = CharField(max_length=30, null=False, default='')
    allocated_gb = DecimalField(decimal_places=1, max_digits=5, null=False, default=0)
    used_gb = DecimalField(decimal_places=1, max_digits=5, null=False, default=0)
    used_pct = DecimalField(decimal_places=1, max_digits=3, null=False, default=0)
    error_cnt = IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    error_msg = CharField(max_length=2000, null=False, default='')

class Metrics_CpuLoad(models.Model):
    class Meta:
        db_table = 'metrics_cpu_load'

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    load_1min = DecimalField(validators=[MinValueValidator(0)], decimal_places=2, max_digits=4, null=False, default=0)
    load_5min = DecimalField(validators=[MinValueValidator(0)], decimal_places=2, max_digits=4, null=False, default=0)
    load_15min = DecimalField(validators=[MinValueValidator(0)], decimal_places=2, max_digits=4, null=False, default=0)
    error_cnt = IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    error_msg = CharField(max_length=2000, null=False, default='')

class Metrics_PingServer(models.Model):
    class Meta:
        db_table = 'metrics_ping_server'

    class PingStatusChoices(DjangoChoices):
        NORMAL = ChoiceItem("Normal", "Normal", 1)
        CRITICAL = ChoiceItem("Critical", "Critical", 2)
        BLACKOUT = ChoiceItem("Blackout", "Blackout", 3)

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    ping_status = CharField(max_length=30, null=False, choices=PingStatusChoices.choices, default='')
    ping_response_ms = IntegerField(null=False, default=0)
    error_cnt = IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    error_msg = CharField(max_length=2000, null=False, default='')

class Metrics_PingDb(models.Model):
    class Meta:
        db_table = 'metrics_ping_db'

    class PingStatusChoices(DjangoChoices):
        NORMAL = ChoiceItem("Normal", "Normal", 1)
        CRITICAL = ChoiceItem("Critical", "Critical", 2)
        BLACKOUT = ChoiceItem("Blackout", "Blackout", 3)

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    ping_db_status = CharField(max_length=30, null=False, choices=PingStatusChoices.choices, default='')
    ping_db_response_ms = IntegerField(null=False, default=0)
    error_cnt = IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    error_msg = CharField(max_length=2000, null=False, default='')

class Metrics_HostDetail(models.Model):
    class Meta:
        db_table = 'metrics_host_detail'

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    ipAddress = CharField(max_length=20, null=True, blank=True)
    last_reboot = DateTimeField(null=True, blank=True)
    cpu = IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    ram_gb = IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    os_version = CharField(max_length=40, null=True, blank=True)
    db_version = CharField(max_length=30, null=True, blank=True)
    db_version_number = IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    error_cnt = IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    error_msg = CharField(max_length=2000, null=False, default='')


class Metrics_CollectionError(models.Model):
    class Meta:
        db_table = 'metrics_collections_error'

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    created_dttm = DateTimeField(editable=False, null=False)
    metric_name = CharField(max_length=40, null=False, blank=True)
    error_cnt = IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    error_msg = CharField(max_length=2000, null=False, default='')

# TODO: Metrics_DbTopSql

