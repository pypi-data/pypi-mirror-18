## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${self.global_title()} &raquo; ${capture(self.title)}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1" />
    ${h.javascript_link('https://code.jquery.com/jquery-1.12.4.min.js')}
    ${h.javascript_link('https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js')}
    ${h.stylesheet_link('https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css')}
    % if not request.rattail_config.production():
        <style type="text/css">
          .ui-page-theme-a { background-image: url(${request.static_url('tailbone:static/img/testing.png')}); }
        </style>
    % endif
  </head>

  <body>
    <div data-role="page">

      <div data-role="header">
        ${h.link_to("Home", url('mobile.home'), class_='ui-btn-left')}
        ${h.link_to("About", url('mobile.about'), class_='ui-btn-right')}
        <h1>${self.global_title()}</h1>
      </div>

      <div role="main" class="ui-content">
        % if capture(self.title):
            <h2>${self.title()}</h2>
        % endif
        ${self.body()}
      </div>

      <div data-role="footer">
        <h4>powered by ${h.link_to("Rattail", url('mobile.about'))}</h4>
      </div>

    </div>
  </body>
</html>

<%def name="global_title()">${"[STAGE] " if not request.rattail_config.production() else ''}Rattail Demo</%def>
