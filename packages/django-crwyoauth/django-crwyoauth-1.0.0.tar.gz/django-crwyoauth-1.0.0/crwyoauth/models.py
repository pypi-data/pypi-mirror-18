#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create,
# modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field
# names.

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CrwyoauthConfig(models.Model):
    OAUTH_TO_CHOICE = (
        ('SINA', 'SINA'),
        ('QQ', 'QQ'),
        ('GITHUB', 'GITHUB')
    )
    oauth_to = models.CharField(unique=True, choices=OAUTH_TO_CHOICE,
                                max_length=100, verbose_name=_('TARGET_OAUTH'))
    authorize_url = models.CharField(max_length=100,
                                     verbose_name='AUTHORIZE_URL')
    client_id = models.CharField(max_length=100, verbose_name='CLIENT_ID')
    client_secret = models.CharField(max_length=100,
                                     verbose_name='CLIENT_SECRET')
    call_back = models.CharField(max_length=100, verbose_name='CALL_BACK')

    class Meta:
        # managed = False
        db_table = 'crwyoauth_config'
        verbose_name = _('CRWY_OAUTH')
        verbose_name_plural = verbose_name
