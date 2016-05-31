from django.utils.translation import ugettext_lazy as _
from django.db import models


class Asterisk(models.Model):
    """
    https://wiki.asterisk.org/wiki/display/AST/PostgreSQL+CDR+Backend

    CREATE TABLE cdr (
            billsec int NOT NULL DEFAULT '0',
            duration int NOT NULL DEFAULT '0',
            amaflags int NOT NULL DEFAULT '0',
            sequence int NOT NULL DEFAULT '0',
            src varchar (80) NOT NULL DEFAULT '',
            dst varchar (80) NOT NULL DEFAULT '',
            clid varchar (80) NOT NULL DEFAULT '',
            calldate timestamp NOT NULL DEFAULT '1970-01-18 00:00:00',
            channel varchar (80) NOT NULL DEFAULT '',
            lastapp varchar (80) NOT NULL DEFAULT '',
            lastdata varchar (80) NOT NULL DEFAULT '',
            dcontext varchar (80) NOT NULL DEFAULT '',
            linkedid varchar(150) NOT NULL DEFAULT '',
            uniqueid varchar (150) NOT NULL DEFAULT '',
            dstchannel varchar (80) NOT NULL DEFAULT '',
            userfield varchar (255) NOT NULL DEFAULT '',
            peeraccount varchar(20) NOT NULL DEFAULT '',
            disposition varchar (45) NOT NULL DEFAULT '',
            accountcode varchar (20) NOT NULL DEFAULT ''
    );
    """

    uniqueid = models.CharField(primary_key=True, max_length=150, verbose_name=_('uniqueid'))
    calldate = models.DateTimeField(auto_now=False, auto_now_add=False, db_index=True,
                                    default='1970-01-18 00:00:00', verbose_name=_('call date'))
    billsec = models.IntegerField(verbose_name=_('BillSec'))
    duration = models.IntegerField(verbose_name=_('Duration'))
    amaflags = models.IntegerField(verbose_name=_('amaflags'))
    sequence = models.IntegerField(verbose_name=_('sequence'))
    src = models.CharField(max_length=80, verbose_name=_('Source number'))
    dst = models.CharField(max_length=80, db_index=True, verbose_name=_('Destination number'))
    clid = models.CharField(max_length=80, verbose_name=_('Input channel'))
    channel = models.CharField(max_length=80, verbose_name=_('channel'))
    lastapp = models.CharField(max_length=80, verbose_name=_('lastapp'))
    dcontext = models.CharField(max_length=80, verbose_name=_('dcontext'))
    lastdata = models.CharField(max_length=80, verbose_name=_('lastdata'))
    linkedid = models.CharField(max_length=150, verbose_name=_('linkedid'))
    userfield = models.CharField(max_length=255, verbose_name=_('userfield'))
    dstchannel = models.CharField(max_length=80, verbose_name=_('Output channel'))
    disposition = models.CharField(max_length=80, verbose_name=_('Call status'))
    peeraccount = models.CharField(max_length=20, verbose_name=_('peeraccount'))
    accountcode = models.CharField(max_length=20, db_index=True, verbose_name=_('accountcode'))

    # class Meta:
    #     managed = False
