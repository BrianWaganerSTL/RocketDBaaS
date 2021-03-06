from django.db import models
from django.db.models import ForeignKey, IntegerField, CASCADE, deletion, BooleanField, CharField, DateTimeField, DecimalField
from djchoices import DjangoChoices, ChoiceItem
from rest_framework.compat import MinValueValidator, MaxValueValidator

from dbaas.models import Server, Application


# ========================================================================
class ThresholdNotificationMethodLookup(models.Model):
  class Meta:
    db_table = 'monitor_threshold_notification_method_lookup'

  notification_method = CharField(max_length=15, null=False, default='')
  created_dttm = DateTimeField(editable=False, auto_now_add=True)
  updated_dttm = DateTimeField(auto_now=True)
  active_sw = BooleanField(default=True, null=False)

  def __str__(self):
    return str(self.notification_method)


class ThresholdCategoryLookup(models.Model):
  class Meta:
    db_table = 'monitor_threshold_category_lookup'

  category_name = CharField(max_length=30, null=False, default='')
  created_dttm = DateTimeField(editable=False, auto_now_add=True)
  updated_dttm = DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.category_name)


class ThresholdMetricLookup(models.Model):
  class Meta:
    db_table = 'monitor_threshold_metric_lookup'

  category = ForeignKey(ThresholdCategoryLookup, on_delete=CASCADE, default='')
  metric_name = CharField(max_length=30, null=False, default='')
  detail_element_sw = BooleanField(default=False, null=False)
  created_dttm = DateTimeField(editable=False, auto_now_add=True)
  updated_dttm = DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.metric_name)

class PredicateTypeChoices(DjangoChoices):
  GTE = ChoiceItem(">=", ">=", 1)
  GTH = ChoiceItem(">", ">", 2)
  EQ = ChoiceItem("==", "==", 3)
  NE = ChoiceItem("!=", "!=", 4)
  LTE = ChoiceItem("<=", "<=", 5)
  LTH = ChoiceItem("<", "<", 6)

class ThresholdTest(models.Model):
  class Meta:
    db_table = 'monitor_threshold_test'

  threshold_metric = ForeignKey(ThresholdMetricLookup, on_delete=CASCADE, default='')
  detail_element = CharField(max_length=50, null=True, blank=True)
  normal_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
  warning_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
  warning_predicate_type = CharField(max_length=15, null=False, choices=PredicateTypeChoices.choices, default=PredicateTypeChoices.GTE)
  warning_value = CharField(max_length=100, null=False, default='')
  critical_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
  critical_predicate_type = CharField(max_length=15, null=False, choices=PredicateTypeChoices.choices, default=PredicateTypeChoices.GTE)
  critical_value = CharField(max_length=100, null=False, default='')
  notification_method = ForeignKey(ThresholdNotificationMethodLookup, on_delete=CASCADE, default='')
  active_sw = BooleanField(default=True, null=False)
  created_dttm = DateTimeField(editable=False, auto_now_add=True)
  updated_dttm = DateTimeField(auto_now=True)


class Incident(models.Model):
  class Meta:
    db_table = 'monitor_incident'
    ordering = ['-last_dttm']

  class StatusChoices(DjangoChoices):
    NORMAL = ChoiceItem("Normal", "Normal", 1)
    WARNING = ChoiceItem("Warning", 'Warning', 2)
    CRITICAL = ChoiceItem("Critical", "Critical", 3)
    BLACKOUT = ChoiceItem("Blackout", "Blackout", 4)
    UNKNOWN = ChoiceItem("Unknown", "Unknown", 5)
    WATCHING = ChoiceItem("Watching", "Watching", 6)

  server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
  threshold_test = ForeignKey(ThresholdTest, on_delete=deletion.ProtectedError, null=False, default='')
  start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
  last_dttm = DateTimeField()
  closed_dttm = DateTimeField(null=True, blank=True)
  closed_sw = BooleanField(default=False)
  min_value = DecimalField(null=False, max_digits=6, decimal_places=2, default=0)
  cur_value = DecimalField(null=False, max_digits=6, decimal_places=2, default=0)
  max_value = DecimalField(null=False, max_digits=6, decimal_places=2, default=0)
  cur_test_w_values = CharField(max_length=500, null=False, default='')
  pending_status = CharField(max_length=15, null=False, default='', choices=StatusChoices.choices)
  current_status = CharField(max_length=15, null=False, choices=StatusChoices.choices, default=StatusChoices.WATCHING)
  max_status = CharField(max_length=15, null=False, choices=StatusChoices.choices, default=StatusChoices.WATCHING)
  detail_element = CharField(max_length=25, null=False, default='')
  critical_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
  warning_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
  normal_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
  note = CharField(max_length=4000, null=True, blank=True)
  note_by = CharField(max_length=30, null=True, blank=True)
  ticket = CharField(max_length=30, null=True, blank=True)
  created_dttm = DateTimeField(editable=False, auto_now_add=True)
  updated_dttm = DateTimeField(auto_now=True)


class IncidentDetail(models.Model):
  class Meta:
    db_table = 'monitor_incident_details'
    ordering = ['-created_dttm']

  incident = ForeignKey(Incident, on_delete=deletion.CASCADE, null=False)
  cur_value = DecimalField(null=False, max_digits=6, decimal_places=2, default=0)
  min_value = DecimalField(null=False, max_digits=6, decimal_places=2, default=0)
  max_value = DecimalField(null=False, max_digits=6, decimal_places=2, default=0)
  cur_test_w_values = CharField(max_length=500, null=False, default='')
  max_status = CharField(max_length=15, null=False, choices=Incident.StatusChoices.choices, default=Incident.StatusChoices.WATCHING)
  pending_status = CharField(max_length=15, null=False, choices=Incident.StatusChoices.choices, default=Incident.StatusChoices.WATCHING)
  current_status = CharField(max_length=15, null=False, choices=Incident.StatusChoices.choices, default=Incident.StatusChoices.WATCHING)
  critical_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
  warning_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
  normal_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
  created_dttm = DateTimeField(editable=False, auto_now_add=True)


class IncidentNotification(models.Model):
  class Meta:
    db_table = 'monitor_incident_notification'

  incident = ForeignKey(Incident, on_delete=deletion.CASCADE, null=True)
  application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=True)
  notification_dttm = DateTimeField(editable=False, auto_now_add=True)
  notification_method = ForeignKey(ThresholdNotificationMethodLookup, on_delete=CASCADE, default='')
  notification_subject = CharField(max_length=2000, null=False, default='')
  notification_body = CharField(max_length=10000, null=False, default='')
  acknowledged_by = CharField(max_length=30, null=True, blank=True)
  acknowledged_dttm = DateTimeField(null=True, blank=True)
  created_dttm = DateTimeField(editable=False, auto_now_add=True)
  updated_dttm = DateTimeField(auto_now=True)
  error_msg = CharField(max_length=2000, null=True, blank=True)
