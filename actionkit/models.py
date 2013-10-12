from django.db import models

class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = u'reports_report'
        managed = False

class QueryReport(models.Model):
    report_ptr = models.ForeignKey(Report, primary_key=True)
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
    #lang = models.ForeignKey(CoreLanguage, null=True, blank=True)
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

class CoreUserField(models.Model):
    parent = models.ForeignKey(CoreUser, related_name='fields')
    name = models.TextField()
    value = models.TextField()
    class Meta:
        db_table = 'core_userfield'
        managed = False

class CoreLocation(models.Model):
    user = models.OneToOneField(CoreUser, related_name="location", primary_key=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    us_district = models.TextField(null=True, blank=True)

    class Meta:
        db_table = u'core_location'
        managed = False
    
class CorePhone(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(CoreUser, related_name="phone")
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
    #hosted_with = models.ForeignKey(CoreHostingplatform)
    url = models.CharField(max_length=765)
    type = models.CharField(max_length=765)
    #lang = models.ForeignKey(CoreLanguage, null=True, blank=True)
    #english_version = models.ForeignKey('self', null=True, blank=True)
    goal = models.IntegerField(null=True, blank=True)
    goal_type = models.CharField(max_length=765)
    status = models.CharField(max_length=765)
    #list = models.ForeignKey(CoreList)
    hidden = models.IntegerField()
    class Meta:
        db_table = u'core_page'
        managed = False

class CoreAction(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser,related_name="action")
    #mailing = models.ForeignKey(CoreMailing, null=True, blank=True,related_name="related_mailer")
    page = models.ForeignKey(CorePage)
    link = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=765)
    opq_id = models.CharField(max_length=765)
    created_user = models.IntegerField()
    subscribed_user = models.IntegerField()
    #referring_user = models.ForeignKey(CoreUser, null=True, blank=True)
    #referring_mailing = models.ForeignKey(CoreMailing, null=True, blank=True)
    status = models.CharField(max_length=765)
    taf_emails_sent = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'core_action'
        managed = False
        
class CoreActionField(models.Model):
    parent = models.ForeignKey(CoreAction, related_name='fields')
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
    page = models.ForeignKey(CorePage, related_name="pagetags")
    tag = models.ForeignKey(CoreTag, related_name="pagetags")
    class Meta:
        db_table = u'core_page_tags'
        managed = False

class CoreOrder(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(CoreUser, related_name="orders")
    action = models.ForeignKey(CoreAction, related_name="orders")
    total = models.FloatField(max_length=255, unique=True)
    status = models.CharField(max_length=255)
    class Meta:
        db_table = u'core_order'
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
    mailing = models.ForeignKey(CoreMailing)
    class Meta:
        db_table = u'core_mailingsubject'
        managed = False

class CoreClickUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    page = models.ForeignKey(CorePage)
    class Meta:
        db_table = u'core_clickurl'
        managed = False

class CoreClick(models.Model):
    clickurl = models.ForeignKey(CoreClickUrl)
    user = models.ForeignKey(CoreUser)
    mailing = models.ForeignKey(CoreMailing)
    link_number = models.IntegerField(null=True)
    source = models.CharField(max_length=255)
    referring_user_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(primary_key=True)
    class Meta:
        db_table = u'core_click'
        managed = False

class CoreOpen(models.Model):
    user = models.ForeignKey(CoreUser, related_name="email_opens")
    mailing = models.ForeignKey(CoreMailing)
    created_at = models.DateTimeField(primary_key=True)
    class Meta:
        db_table = u'core_open'
        managed = False

class CoreUserMailing(models.Model):
    mailing = models.ForeignKey(CoreMailing)
    user = models.ForeignKey(CoreUser)
    subject = models.ForeignKey(CoreMailingSubject)
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

class CmsPetitionForm(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.OneToOneField(CorePage)
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
    page = models.OneToOneField(CorePage)

    class Meta:
        db_table = u'core_pagefollowup'
        managed = False
