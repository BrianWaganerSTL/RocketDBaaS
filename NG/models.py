from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model, CharField, DecimalField, BooleanField, DateTimeField, IntegerField, EmailField, ForeignKey, deletion
from django.utils import timezone


DBMS_TYPES = (
    ('PostgreSQL', 'PostgreSQL'),
    ('MongoDB', 'MongoDB'),
)


class PoolServer(Model):
    serverName = CharField(max_length=30, null=False)
    serverIp = CharField(max_length=14, null=False)
    dbms = CharField(choices=DBMS_TYPES, max_length=10, null=False)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    memGigs = DecimalField(decimal_places=1, max_digits=3, null=False)
    dbGigs = DecimalField(decimal_places=2, max_digits=4, null=False)
    dataCenter = CharField(max_length=20, null=False)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.serverName


class Environment(Model):
    envName = CharField(max_length=5, null=False)
    envFullName = CharField(max_length=25, null=False)
    activeSw = BooleanField(null=False)

    def __str__(self):
        return self.envName


class Contact(Model):
    contactName = CharField(max_length=60, null=False)
    contactType = CharField(max_length=30)
    email = EmailField
    phone = CharField(max_length=15)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.contactName


class Application(Model):
    appName = CharField(max_length=40, null=False)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.appName


class Cluster(Model):
    clusterName = CharField(max_length=30, null=False)
    dbms = CharField(choices=DBMS_TYPES, max_length=10, null=False)
    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    environment = ForeignKey(Environment, on_delete=deletion.ProtectedError, null=False)
    requestedCpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    requestedMemGigs = DecimalField(decimal_places=1, max_digits=3, null=False)
    requestedDbGigs = DecimalField(decimal_places=2, max_digits=4, null=False)
    haPort = IntegerField(validators=[MaxValueValidator(9999)])
    tlsEnabled = BooleanField(null=False)
    backupRetentionDays = IntegerField(validators=[MinValueValidator(1),MaxValueValidator(30)], null=False)
    health = CharField(max_length=20, null=False)
    activeSw = BooleanField(null=False)
    effDttm = DateTimeField(default=timezone.now)
    expDttm = DateTimeField
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.clusterName


class Server(Model):
    cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=False)
    serverName = CharField(max_length=30, null=False)
    serverIp = CharField(max_length=14, null=False)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    memGigs = DecimalField(decimal_places=1, max_digits=3, null=False)
    dbGigs = DecimalField(decimal_places=2, max_digits=4, null=False)
    dataCenter = CharField(max_length=20, null=False)
    arbiterNodeSw = BooleanField(null=False)
    osVersion = CharField(max_length=30)
    dbVersion = CharField(max_length=30)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.serverName




class ApplicationContact(Model):
    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    contact = ForeignKey(Contact, on_delete=deletion.ProtectedError, null=False)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.application.appName + ': ' + self.contact.contactName