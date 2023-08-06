## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Login</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/login.js'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/login.css'))}
</%def>

<%def name="logo()">
  ${h.image(request.static_url('tailbone:static/img/home_logo.png'), "Rattail Logo", id='logo')}
</%def>

<%def name="login_form()">
  <div class="form">
    ${form.begin(**{'data-ajax': 'false'})}
    ${form.hidden('referrer', value=referrer)}
    ${form.csrf_token()}

    ${form.field_div('username', form.text('username'))}
    ${form.field_div('password', form.password('password'))}

    <div class="buttons">
      ${form.submit('submit', "Login")}
      <input type="reset" value="Reset" />
    </div>

    ${form.end()}
  </div>
</%def>

${self.logo()}

${self.login_form()}
