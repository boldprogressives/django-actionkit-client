from django.db import models

class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    description = models.TextField()

    class Meta:
        db_table = u'reports_report'
        managed = False

class QueryReport(models.Model):
    report_ptr = models.ForeignKey(Report, primary_key=True, on_delete=models.DO_NOTHING)
    sql = models.TextField()
    class Meta:
        db_table = u'reports_queryreport'
        managed = False

class CoreLanguage(models.Model):
    name = models.TextField()
    class Meta:
        db_table = u'core_language'
        managed = False

class CoreUser(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255)
    prefix = models.CharField(max_length=765)
    first_name = models.CharField(max_length=765)
    middle_name = models.CharField(max_length=765)
    last_name = models.CharField(max_length=765)
    suffix = models.CharField(max_length=765)
    password = models.CharField(max_length=765)
    subscription_status = models.CharField(max_length=765)
    address1 = models.CharField(max_length=765)
    address2 = models.CharField(max_length=765)
    city = models.CharField(max_length=765)
    state = models.CharField(max_length=765)
    region = models.CharField(max_length=765)
    postal = models.CharField(max_length=765)
    zip = models.CharField(max_length=15)
    plus4 = models.CharField(max_length=12)
    country = models.CharField(max_length=765)
    source = models.CharField(max_length=765)
    lang = models.ForeignKey(CoreLanguage, null=True, blank=True, on_delete=models.DO_NOTHING)
    rand_id = models.IntegerField()
    class Meta:
        db_table = u'core_user'
        managed = False

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def formatted_address(self):
        fields = [
            self.address1,
            self.address2,
            self.city,
            self.state,
            self.region,
            self.zip,
            self.country
            ]
        return u", ".join(field for field in fields
                          if field and field.strip())

class CoreUserMerge(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    primary = models.ForeignKey(CoreUser, related_name='merges', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255)
    class Meta:
        db_table = u'core_usermerge'
        managed = False


class CoreUserMergeUsers(models.Model):
    id = models.IntegerField(primary_key=True)
    usermerge = models.ForeignKey(CoreUserMerge, related_name='mergeusers', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, related_name='mergeusers', on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u'core_usermerge_users'
        managed = False


class CoreList(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.BooleanField()
    name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField()

    class Meta:
        db_table = u'core_list'
        managed = False    
    
class CoreSubscription(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, on_delete=models.DO_NOTHING)
    list = models.ForeignKey(CoreList, on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table = u'core_subscription'
        managed = False

class CoreSubscriptionHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, on_delete=models.DO_NOTHING)
    list = models.ForeignKey(CoreList, on_delete=models.DO_NOTHING)
    change_id = models.IntegerField()
    
    class Meta:
        db_table = u'core_subscriptionhistory'
        managed = False

class CoreUserField(models.Model):
    parent = models.ForeignKey(CoreUser, related_name='fields', on_delete=models.DO_NOTHING)
    name = models.TextField()
    value = models.TextField()
    class Meta:
        db_table = 'core_userfield'
        managed = False

class CoreLocation(models.Model):
    user = models.OneToOneField(CoreUser, related_name="location", primary_key=True, on_delete=models.DO_NOTHING)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    us_district = models.TextField(null=True, blank=True)

    class Meta:
        db_table = u'core_location'
        managed = False
    
class CorePhone(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(CoreUser, related_name="phone", on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    normalized_phone = models.CharField(max_length=25)
    class Meta:
        db_table = u'core_phone'
        managed = False

    def __unicode__(self):
        if self.phone:
            return u"%s%s" % (self.phone, (
                    self.type and " (%s)" % self.type or ''))
        return u''

class CorePage(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=765)
    name = models.CharField(max_length=765)
    #hosted_with = models.ForeignKey(CoreHostingplatform, on_delete=models.DO_NOTHING)
    notes = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=765)
    type = models.CharField(max_length=765)
    #lang = models.ForeignKey(CoreLanguage, null=True, blank=True, on_delete=models.DO_NOTHING)
    #english_version = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)
    goal = models.IntegerField(null=True, blank=True)
    goal_type = models.CharField(max_length=765)
    status = models.CharField(max_length=765)
    list = models.ForeignKey(CoreList, on_delete=models.DO_NOTHING)
    hidden = models.IntegerField()
    allow_multiple_responses = models.BooleanField()
    
    class Meta:
        db_table = u'core_page'
        managed = False

class CorePageField(models.Model):
    parent = models.ForeignKey(CorePage, related_name='fields', on_delete=models.DO_NOTHING)
    name = models.TextField()
    value = models.TextField()
    class Meta:
        db_table = 'core_pagefield'
        managed = False


class CoreAction(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser,related_name="action", on_delete=models.DO_NOTHING)
    #mailing = models.ForeignKey(CoreMailing, null=True, blank=True,related_name="related_mailer", on_delete=models.DO_NOTHING)
    page = models.ForeignKey(CorePage, on_delete=models.DO_NOTHING)
    link = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=765)
    opq_id = models.CharField(max_length=765)
    created_user = models.IntegerField()
    subscribed_user = models.IntegerField()
    #referring_user = models.ForeignKey(CoreUser, null=True, blank=True, on_delete=models.DO_NOTHING)
    #referring_mailing = models.ForeignKey(CoreMailing, null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=765)
    taf_emails_sent = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'core_action'
        managed = False
        
class CoreActionField(models.Model):
    parent = models.ForeignKey(CoreAction, related_name='fields', on_delete=models.DO_NOTHING)
    name = models.TextField()
    value = models.TextField()
    class Meta:
        db_table = 'core_actionfield'
        managed = False

class CoreTag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = u'core_tag'
        managed = False
    
class CorePageTag(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.ForeignKey(CorePage, related_name="pagetags", on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(CoreTag, related_name="pagetags", on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u'core_page_tags'
        managed = False


class CoreOrder(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, related_name="orders", on_delete=models.DO_NOTHING)
    action = models.ForeignKey(CoreAction, related_name="orders", on_delete=models.DO_NOTHING)
    total = models.FloatField()
    status = models.CharField(max_length=255)
    import_id = models.CharField(max_length=32, null=True)
    card_num_last_four = models.CharField(max_length=32, null=True)
    class Meta:
        db_table = u'core_order'
        managed = False

class CoreTransaction(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=255)
    order = models.ForeignKey(CoreOrder, related_name="transactions", on_delete=models.DO_NOTHING)
    account = models.CharField(max_length=255)
    amount = models.FloatField()
    success = models.BooleanField()
    status = models.CharField(max_length=255)
    class Meta:
        db_table = u'core_transaction'
        managed = False

class CoreOrderRecurring(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(CoreOrder, related_name="recurrences", on_delete=models.DO_NOTHING)
    action = models.ForeignKey(CoreAction, related_name="recurrences", on_delete=models.DO_NOTHING)
    exp_date = models.CharField(max_length=6)
    recurring_id = models.CharField(max_length=255)
    account = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CoreUser, related_name="recurrences", on_delete=models.DO_NOTHING)
    start = models.DateField()
    occurrences = models.IntegerField(null=True)
    period = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.CharField(max_length=255)
    class Meta:
        db_table = u'core_orderrecurring'
        managed = False

class CoreMailing(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    html = models.TextField()
    text = models.TextField()
    status = models.CharField(max_length=255)
    class Meta:
        db_table = u'core_mailing'
        managed = False

class CoreMailingSubject(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    text = models.CharField(max_length=255)
    mailing = models.ForeignKey(CoreMailing, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u'core_mailingsubject'
        managed = False

class CoreClickUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    page = models.ForeignKey(CorePage, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u'core_clickurl'
        managed = False

class CoreClick(models.Model):
    clickurl = models.ForeignKey(CoreClickUrl, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, on_delete=models.DO_NOTHING)
    mailing = models.ForeignKey(CoreMailing, on_delete=models.DO_NOTHING)
    link_number = models.IntegerField(null=True)
    source = models.CharField(max_length=255)
    referring_user_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(primary_key=True)
    class Meta:
        db_table = u'core_click'
        managed = False

class CoreOpen(models.Model):
    user = models.ForeignKey(CoreUser, related_name="email_opens", on_delete=models.DO_NOTHING)
    mailing = models.ForeignKey(CoreMailing, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(primary_key=True)
    class Meta:
        db_table = u'core_open'
        managed = False

class CoreUserMailing(models.Model):
    mailing = models.ForeignKey(CoreMailing, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(CoreMailingSubject, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(primary_key=True)    
    class Meta:
        db_table = u'core_usermailing'
        managed = False

    def to_json(self):
        return dict(
            created_at=self.created_at,
            subject_text=self.subject.text,
            )

class EventCampaign(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    title = models.CharField(max_length=765)
    name = models.CharField(max_length=765)
    
    public_create_page = models.BooleanField()
    public_search_page = models.BooleanField()
    use_title = models.BooleanField()
    show_title = models.BooleanField()
    show_venue = models.BooleanField()
    show_address1 = models.BooleanField()
    show_city = models.BooleanField()
    show_state = models.BooleanField()
    show_zip = models.BooleanField()
    show_public_description = models.BooleanField()
    show_directions = models.BooleanField()
    show_attendee_count = models.BooleanField()

    starts_at = models.DateTimeField(null=True)
    
    use_start_date = models.BooleanField()
    use_start_time = models.BooleanField()
    require_staff_approval = models.BooleanField()
    require_email_confirmation = models.BooleanField()
    allow_private = models.BooleanField()

    max_event_size = models.IntegerField(null=True)
    default_event_size = models.IntegerField(null=True)

    default_title = models.CharField(max_length=255)

    class Meta:
        db_table = "events_campaign"
        managed = False

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    address1 = models.CharField(max_length=765)
    address2 = models.CharField(max_length=765)
    city = models.CharField(max_length=765)
    state = models.CharField(max_length=765)
    region = models.CharField(max_length=765)
    postal = models.CharField(max_length=765)
    zip = models.CharField(max_length=15)
    plus4 = models.CharField(max_length=12)
    country = models.CharField(max_length=765)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    campaign = models.ForeignKey(EventCampaign, on_delete=models.DO_NOTHING)

    title = models.CharField(max_length=765)

    creator = models.ForeignKey(CoreUser, on_delete=models.DO_NOTHING)

    starts_at = models.DateTimeField(null=True)
    ends_at = models.DateTimeField(null=True)    

    status = models.CharField(max_length=32)
    host_is_confirmed = models.BooleanField()
    is_private = models.BooleanField()
    is_approved = models.BooleanField()
    attendee_count = models.IntegerField()
    max_attendees = models.IntegerField()

    venue = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    public_description = models.TextField()
    directions = models.TextField()
    note_to_attendees = models.TextField()
    notes = models.TextField()
    starts_at_utc = models.DateTimeField(null=True)
    ends_at_utc = models.DateTimeField(null=True)

    class Meta:
        db_table = "events_event"
        managed = False

class Eventfield(models.Model):
    parent = models.ForeignKey(Event, related_name='fields', on_delete=models.DO_NOTHING)
    name = models.TextField()
    value = models.TextField()
    class Meta:
        db_table = 'events_eventfield'
        managed = False

class EventSignup(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    page = models.ForeignKey(CorePage, on_delete=models.DO_NOTHING)
    attended = models.BooleanField(default=False)

    class Meta:
        db_table = "events_eventsignup"
        managed = False


class CmsPetitionForm(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.OneToOneField(CorePage, on_delete=models.DO_NOTHING)
    templateset_id = models.IntegerField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    client_hosted = models.BooleanField()
    client_url = models.CharField(max_length=255, blank=True)
    
    thank_you_text = models.TextField()
    statement_leadin = models.TextField()
    statement_text = models.TextField()
    about_text = models.TextField()
    
    class Meta:
        db_table = u'cms_petition_form'
        managed = False

class CorePageFollowup(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.OneToOneField(CorePage, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = u'core_pagefollowup'
        managed = False

from django.db import connections
try:
    from django.utils.datastructures import SortedDict
except ImportError:
    from collections import OrderedDict as SortedDict

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        SortedDict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def opens_by_user(user):
    cursor = connections['ak'].cursor()
    sql = """
SELECT open.mailing_id, open.created_at,
       subject.text AS subject_text,
       mailing.created_at AS mailed_at
FROM core_open open
LEFT JOIN core_mailing mailing
  ON mailing.id=open.mailing_id
LEFT JOIN core_usermailing usermailing
  ON open.mailing_id=usermailing.mailing_id 
  AND open.user_id=usermailing.user_id
LEFT JOIN core_mailingsubject subject 
  ON subject.id=usermailing.subject_id
WHERE open.user_id=%s
ORDER BY created_at DESC"""
    cursor.execute(sql, [user.id])
    return dictfetchall(cursor)

def clicks_by_user(user):
    cursor = connections['ak'].cursor()
    sql = """
SELECT click.mailing_id, click.created_at, 
       subject.text AS subject_text,
       mailing.created_at AS mailed_at
FROM core_click click
LEFT JOIN core_mailing mailing 
  ON mailing.id=click.mailing_id
LEFT JOIN core_usermailing usermailing
  ON click.mailing_id=usermailing.mailing_id 
  AND click.user_id=usermailing.user_id
LEFT JOIN core_mailingsubject subject 
  ON subject.id=usermailing.subject_id
WHERE click.user_id=%s
ORDER BY created_at DESC"""
    cursor.execute(sql, [user.id])
    return dictfetchall(cursor)

def mailings_by_user(user):
    cursor = connections['ak'].cursor()
    sql = """
SELECT usermailing.id as usermailing_id,
       mailing.id as id,
       mailing.created_at as mailed_at,
       click.created_at as clicked_at, 
       subject.text AS subject_text,
       open.created_at as opened_at
FROM core_usermailing usermailing
LEFT JOIN core_mailingsubject subject 
  ON subject.id=usermailing.subject_id
LEFT JOIN core_mailing mailing
  ON mailing.id=usermailing.mailing_id
LEFT JOIN core_click click
  ON click.mailing_id=usermailing.mailing_id
  AND click.user_id=usermailing.user_id
LEFT JOIN core_open open
  ON open.mailing_id=usermailing.mailing_id
  AND open.user_id=usermailing.user_id
WHERE usermailing.user_id=%s
ORDER BY usermailing.created_at DESC"""
    cursor.execute(sql, [user.id])
    return dictfetchall(cursor)

