#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..extensions import db


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config = db.Column(db.String())
    value = db.Column(db.String())


    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  
