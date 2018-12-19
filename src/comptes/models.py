# -*- coding: utf-8 -*-
from datetime                       import timedelta
from django.conf                    import settings
from django.core.urlresolvers       import reverse
from django.db                      import models
from django.db.models               import Q
from django.db.models.signals       import pre_save, post_save
from django.contrib.auth.models     import ( AbstractBaseUser, BaseUserManager )
from django.core.mail               import send_mail
from django.template.loader         import get_template
from django.utils                   import timezone
from sbeeapp.utils                  import random_string_generator, unique_key_generator
from django.core.validators         import RegexValidator

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)


class UserManager(BaseUserManager):
    def create_user(self, email, nom, prenoms, ref_abonne, password=None, is_active=False, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Vous devez ecrire votre addresse email')
        if not nom:
            raise ValueError('Vous devez ecrire votre nom')
        if not prenoms:
            raise ValueError('Vous devez ecrire vos prenoms')
        if not ref_abonne:
            raise ValueError('Vous devez ecrire votre reference abonnée')
        if not password:
            raise ValueError('Vous devez ecrire votre mot de passe')

        user = self.model(
            email=self.normalize_email(email),
            nom = nom,
            prenoms = prenoms,
            ref_abonne = ref_abonne
        )

        #C'est ici que je definis les trucs par defaut

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, nom, prenoms, ref_abonne, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email, nom, prenoms, ref_abonne,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_clientuser(self, email, nom, prenoms, ref_abonne, password):
        """
        Creates and saves a client user with the given email and password.
        """
        user = self.create_user(
            email, nom, prenoms, ref_abonne,
            password=password,
        )
        user.client = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenoms, ref_abonne, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email, nom, prenoms, ref_abonne,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user



#--------------------------------------------------------------------------------------

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    nom = models.CharField(verbose_name='Nom', max_length=255)
    prenoms = models.CharField(verbose_name='Prenom', max_length=255)
    ref_abonne = models.CharField(verbose_name='Reference Abonné', max_length=20, primary_key=True, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Format: '+999999999'. 15 chiffres maximum.")
    telephone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_active= models.BooleanField(default=True)
    client  = models.BooleanField(default=True)
    staff   = models.BooleanField(default=False) # a admin user; non super-user
    admin   = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenoms', 'ref_abonne'] # Email & Password are required by default.

    objects = UserManager()


    # def get_url(self):
    #     return reverse('factures:show', kwargs={'pk': self.pk})

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def get_ref_abonne(self):
        # The user is identified by their email address
        return self.ref_abonne

    def get_url(self):
        return reverse('compte:show', kwargs={'pk': self.pk})

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_client(self):
        "Is the user a member of client?"
        return self.client

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def __iter__(self):
        return iter([self.email, self.nom, self.prenoms])


#--------------------------------------------------------------------------------------

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a timestamp in here
        end_range = now
        return self.filter(
                activated = False,
                forced_expired = False
              ).filter(
                timestamp__gt=start_range,
                timestamp__lte=end_range
              )


#--------------------------------------------------------------------------------------

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
                    Q(email=email) |
                    Q(user__email=email)
                ).filter(
                    activated=False
                )


#--------------------------------------------------------------------------------------

class EmailActivation(models.Model):
    user            = models.ForeignKey(User)
    email           = models.EmailField()
    key             = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=7) # 7 Days
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            # pre activation user signal
            user = self.user
            user.is_active = True
            user.save()
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'https://www.sbeeapp.com')
                key_path = reverse("compte:email-activate", kwargs={'key': self.key}) # use reverse
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = "Verification d'Email"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,
                )
                return sent_mail
        return False



def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_reciever, sender=User)
