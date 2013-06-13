from django.db import models

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
