from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model, CharField, DecimalField, BooleanField, DateTimeField, IntegerField, EmailField, ForeignKey, deletion
from django.utils import timezone
from djchoices import DjangoChoices, ChoiceItem


class EnvironmentChoices(DjangoChoices):
    SBX = ChoiceItem("SBX","Sandbox",1)
    DEV = ChoiceItem("DEV","Development",2)
    QA = ChoiceItem("QA","Quality Assurance",3)
    UAT = ChoiceItem("UAT","User Acceptance Testing",4)
    PRD = ChoiceItem("PRD","Production",5)
    PPD = ChoiceItem("PPD","Post Production",6)


class DbmsTypeChoices(DjangoChoices):
    PostgreSQL = ChoiceItem()
    MongoDB = ChoiceItem()


class DataCenterChoices(DjangoChoices):
    STL = ChoiceItem("STL", "Saint Louis", 1)
    CH = ChoiceItem("CH", "Chicago", 2)
    PA = ChoiceItem("PA", "Piscataway", 3)


class BackupTypeChoices(DjangoChoices):
    BackupFull = ChoiceItem("Full", "Incremental", 1)
    BackupIncremental = ChoiceItem("Incr","Incremental", 2)
    BackupDifferential = ChoiceItem("Diff", "Differential", 3)


class RestoreTypeChoices(DjangoChoices):
    RestoreFull = ChoiceItem("Full", "Restore Full", 1)
    RestoreDB = ChoiceItem("DB","Restore Database", 2)
    RestoreTable = ChoiceItem("Table", "Restore Table", 3)


class ServerActivityTypeChoices(DjangoChoices):
    RestartServer = ChoiceItem("RestartServer", "Restart Server", 1)
    StopServer = ChoiceItem("StopServer", "Stop Server", 2)
    StartServer = ChoiceItem("StartServer", "Start Server", 3)
    RestartDB = ChoiceItem("RestartDB", "Restart Database", 4)
    PromoteDB = ChoiceItem("PromoteDB", "Promote Database", 5)
    DemomoteDB = ChoiceItem("DemoteDB", "Demote Database", 6)


class PoolServer(Model):
    class Meta:
        db_table = "pool_server"

    class StatusInPoolChoices(DjangoChoices):
        Available = ChoiceItem("Available", "Available",1)
        Locked = ChoiceItem("Locked", "Locked for Build",2)
        Used = ChoiceItem("Used", "Used",3)

    environment = CharField(choices=EnvironmentChoices.choices, max_length=20, null=False, blank=True)
    server_name = CharField(max_length=30, null=False)
    server_ip = CharField(max_length=14, null=False)
    dbms_type = CharField(max_length=10, null=False, blank=True, choices=DbmsTypeChoices.choices)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    mem_gb = DecimalField(decimal_places=1, max_digits=3, null=False)
    db_gb = DecimalField(decimal_places=2, max_digits=5, null=False)
    data_center = CharField(max_length=20, null=False, choices=DataCenterChoices.choices)
    status_in_pool = CharField(max_length=20, null=False, blank=True, choices=StatusInPoolChoices.choices)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class Contact(Model):
    class Meta:
        db_table = "contact"

    class ContactTypeChoices(DjangoChoices):
        Person = ChoiceItem("Person","Person",1)
        Group = ChoiceItem("Distro","Email Group Distro",2)
        API = ChoiceItem("API","API Endpoint",3)

    contact_name = CharField(max_length=60, null=False)
    contact_type = CharField(max_length=30, choices=ContactTypeChoices.choices, null=True)
    contact_email = EmailField(blank=True, null=True)
    contact_phone = CharField(max_length=15)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_name


class Application(Model):
    class Meta:
        db_table = "application"

    application_name = CharField(max_length=40, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.application_name


class Cluster(Model):
    class Meta:
        db_table = "cluster"

    class ClusterHealthChoices(DjangoChoices):
        ClusterConfiguring = ChoiceItem("ClusterConfig", "Cluster Configuring", 1)
        ClusterUp = ChoiceItem("ClusterUp","Nodes Up and Healthy", 2)
        ClusterUpWithIssues = ChoiceItem("ClusterUpWithIssues","Primary is Up but something is Not Healthy", 3)
        ClusterDown = ChoiceItem("ClusterDown", "Cluster is Down", 4)
        ClusterOnLineMaint = ChoiceItem("ClusterOnLineMaint","On-Line Maintenance", 5)

    cluster_name = CharField(max_length=30, null=False)
    dbms_type = CharField(choices=DbmsTypeChoices.choices, max_length=10, null=False)
    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    environment = CharField(choices=EnvironmentChoices.choices, max_length=20, null=False, blank=True)
    requested_cpu = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(14)], null=False)
    requested_mem_gb = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(64)], null=False)
    requested_db_gb = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(102400)], null=False)
    haproxy_port = IntegerField(validators=[MinValueValidator(1024), MaxValueValidator(65535)])
    tls_enabled_sw = BooleanField(null=False)
    backup_retention_days = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], null=False)
    cluster_health = CharField(max_length=30, null=False, choices=ClusterHealthChoices.choices, default=ClusterHealthChoices.ClusterConfiguring)
    active_sw = BooleanField(null=False, default=True)
    eff_dttm = DateTimeField(default=timezone.now)
    exp_dttm = DateTimeField
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class Server(Model):
    class Meta:
        db_table="server"

    class NodeRoleChoices(DjangoChoices):
        Primary = ChoiceItem("Primary", "Primary Node",1)
        SecondarySync = ChoiceItem("SecondarySync", "Secondary Node - Replication is Synchronous",2)
        SecondaryAsync = ChoiceItem("SecondaryAsync", "Secondary Node- Replication is Asynchronous",3)
        Arbiter = ChoiceItem("Arbiter", "Arbiter Node",4)

    cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=False)
    server_name = CharField(max_length=30, null=False)
    server_ip = CharField(max_length=14, null=False)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    mem_gb = DecimalField(decimal_places=1, max_digits=3, null=False)
    db_gb = DecimalField(decimal_places=2, max_digits=5, null=False)
    data_center = CharField(max_length=20, null=False, choices=DataCenterChoices.choices)
    node_role = CharField(choices=NodeRoleChoices.choices, max_length=20, null=False, blank=True)
    os_version = CharField(max_length=30)
    db_version = CharField(max_length=30)
    pending_restart_sw = BooleanField(null=False, default=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class ApplicationContact(Model):
    class Meta:
        db_table = "application_contact"

    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    contact = ForeignKey(Contact, on_delete=deletion.ProtectedError, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


# ========================================================================================

class CreateDBInit(models.Model):
    dbms_types = DbmsTypeChoices
    data_centers = DataCenterChoices.labels
    requested_cpu = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(14)], null=False)
    requested_mem_gb = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(64)], null=False)
    requested_db_gb = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(102400)], null=False)


class Backup (models.Model):
    class Meta:
        db_table = "backup"

    cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=True)
    backup_type = CharField(max_length=10, null=False, choices=BackupTypeChoices.choices, default=BackupTypeChoices.BackupFull)
    backup_status = CharField(max_length=15, null=True)
    db_size_gb = DecimalField(decimal_places=2, max_digits=5, null=True)
    backup_size_gb = DecimalField(decimal_places=2, max_digits=5, null=True)
    start_dttm = DateTimeField(editable=True)
    stop_dttm = DateTimeField(editable=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class Restore(models.Model):
    class Meta:
        db_table="restore"

    from_cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=True, related_name='restore_from_cluster')
    to_cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=True, related_name='restore_to_cluster')
    backup_type = CharField(max_length=10, null=False, choices=BackupTypeChoices.choices,
                            default=BackupTypeChoices.BackupFull)
    restore_to_dttm = DateTimeField(editable=True)
    restore_status = CharField(max_length=15, null=True)
    start_dttm = DateTimeField(editable=True)
    stop_dttm = DateTimeField(editable=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class ServerActivities(models.Model):
    class Meta:
        db_table = "server_activities"

    server = ForeignKey(Server, on_delete=deletion.ProtectedError, null=True)
    server_activity = CharField(max_length=20, null=False, choices=ServerActivityTypeChoices.choices,
                                default=ServerActivityTypeChoices.RestartDB)
    activity_status = CharField(max_length=15, null=True)
    start_dttm = DateTimeField(editable=True)
    stop_dttm = DateTimeField(editable=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class ApplicationContactsDetailsView(models.Model):
    class Meta:
        db_table = "application_contacts_details_view"
        managed = False

    application_id = IntegerField
    contact_id = IntegerField
    contact_name = CharField(max_length=60)
    contact_type = CharField(max_length=30)
    contact_phone = CharField(max_length=15)
    active_sw = BooleanField(null=False, default=True)


