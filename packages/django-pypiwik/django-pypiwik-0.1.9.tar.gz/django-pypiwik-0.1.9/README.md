`django-pypiwik` is a django helper application around pypiwik.


# Configuration

`django-piwik` can be configured at the application level (`settings.py`) or on a per-site level.
It requires the [Site framework](https://docs.djangoproject.com/en/dev/ref/contrib/sites/) to be installed and configured.

Global configuration in `settings.py`:

    PIWIK_URL="http://yourpiwikhost/piwik/"
    PIWIK_SITE_ID = 1

If you have only one site, or all of your sites sending requests to the same piwik site, thats all you have to do.

`django-pypiwik` installs the `Piwik configuration` model. Use this model to connect your Django site with an Piwik site.

When using the `PiwikTrackingMiddleware`, the `PIWIK_TRACKING_MIDDLEWARE_EXCLUDE_ADMIN` option controls whether requests in the Django admin site should be tracked or not.

# Usage

## PiwikMixin

The `PiwikMixin` brings an easy to use interface to your views:

    class IndexView(PiwikMixin, TemplateView):
    	template_name = 'index.html'

The `PiwikMixin` adds a `DjangoPiwikTracker` instance to the `context` called `piwik_tracker`. To render the tracking code in your template, call `tracking_code` on it:

    {{piwik_tracker.tracking_code}}

Tracking variables can be set as an attribute on your view class. The names are the same as [pypiwik's](https://code.not-your-server.de/pypiwik.git). To avoid name collisions with your existing class attributes, all tracking variables are prefixed with `piwik_` (so `action_name` becomes `piwik_action_name`):

    class FAQView(PiwikMixin, TemplateView):
    	template_name = 'index.html'
    	piwik_action_name = 'Help / FAQ'

`django-piwik` also accepts callables as tracking variables. The code above is equivalent to the following:


    class FAQView(PiwikMixin, TemplateView):
    	template_name = 'index.html'

    	def piwik_action_name(self):
    	   return 'Help / FAQ'

## track_page_view decorator

`django-pypiwik` includes a decorator called `track_page_view`.

_Note:_ Yes, it's the same name as pypiwiks `track_page_view` decorator. So watch out which one is listed in your imports.

The `track_page_view` decorator will issue a **server-to-server** tracking request after the view has been processed. Note that, by design, this kind of request will have less data than Piwik's Javascript Tracking API.

As with any other Django decorator, you have to decorate the `dispatch` method on your views (if you are using class based views):

    class IndexView(TemplateView):
    	template_name = 'index.html'

        @track_page_view()
    	def dispatch(self, request, *args, **kwargs):
    		return super(IndexView, self).dispatch(request, *args, **kwargs)

The `track_page_view` decorator will not honor the `piwik_*` variables defined on your view. Instead, pass them to the decorator:

        @track_page_view(action_name='Downloads / Index')
    	def dispatch(self, request, *args, **kwargs):
    		return super(IndexView, self).dispatch(request, *args, **kwargs)

You can also use the `track_page_view` decorator in your `urls.py` to wrap third-party views, like Djangos [syndication](https://docs.djangoproject.com/en/1.8/ref/contrib/syndication/) or [sitemap](https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/) framwork:

    from django_pypiwik.decorators import track_page_view

    urlpatterns = [
        # ...
        url(r'^latest/feed/$', track_page_view(track_bots=True)(LatestEntriesFeed())),
    ]

## PiwikTrackingMiddleware (since 0.1.6)

You can also use the `PiwikTrackingMiddleware` to track page views by including `django_pypiwik.middleware.PiwikTrackingMiddleware` in your `MIDDLEWARE_CLASSES`. The middleware sends a server-to-server tracking call in the `process_response` hook.
The `PIWIK_TRACKING_MIDDLEWARE_PARAMS` option (a dict) in your settings.py let you control other tracking parameters to send to Piwik. 

Please note that the call is synchronous - if your tracking server is slow to response, the response time of your application will suffer.


## Passing token_auth

The `token_auth` parameter, required for some tracking variables, can be defined at three levels:

1. `PIWIK_TOKEN_AUTH` in `settings.py`. This is the default `token_auth` value for all sites
1. `PIWIK_PARAMS['token_auth']` in `settings.py`. Same as 1 but allows you to define other default parameters too.
1. As configured in the Piwik configuration (see above) for the current site.

