# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2016 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Various common views
"""

from __future__ import unicode_literals, absolute_import

import rattail
from rattail.mail import send_email
from rattail.util import OrderedDict

import formencode as fe
from pyramid import httpexceptions
from pyramid_simpleform import Form

import tailbone
from tailbone import forms
from tailbone.views import View


class Feedback(fe.Schema):
    """
    Form schema for user feedback.
    """
    allow_extra_fields = True
    user = forms.validators.ValidUser()
    user_name = fe.validators.NotEmpty()
    message = fe.validators.NotEmpty()


class CommonView(View):
    """
    Base class for common views; override as needed.
    """
    project_title = "Tailbone"
    project_version = tailbone.__version__

    def about(self):
        """
        Generic view to show "about project" info page.
        """
        return {
            'project_title': self.project_title,
            'project_version': self.project_version,
            'packages': self.get_packages(),
        }

    def get_packages(self):
        """
        Should return the full set of packages which should be displayed on the
        'about' page.
        """
        return OrderedDict([
            ('rattail', rattail.__version__),
            ('Tailbone', tailbone.__version__),
        ])

    def feedback(self):
        """
        Generic view to present/handle the user feedback form.
        """
        form = Form(self.request, schema=Feedback)
        if form.validate():
            data = dict(form.data)
            if data['user']:
                data['user_url'] = self.request.route_url('users.view', uuid=data['user'].uuid)
            send_email(self.rattail_config, 'user_feedback', data=data)
            self.request.session.flash("Thank you for your feedback.")
            return httpexceptions.HTTPFound(location=form.data['referrer'])
        return {'form': forms.FormRenderer(form)}
    
    @classmethod
    def defaults(cls, config):

        config.add_route('about', '/about')
        config.add_view(cls, attr='about', route_name='about', 
                        renderer='/about.mako')

        config.add_route('feedback', '/feedback')
        config.add_view(cls, attr='feedback', route_name='feedback',
                        renderer='/feedback.mako')


def includeme(config):
    CommonView.defaults(config)
