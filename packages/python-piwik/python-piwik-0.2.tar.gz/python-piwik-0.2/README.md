Python implementation of the Piwik HTTP API.

**Note**: This project is called *python-piwik* on PyPI since *pypiwik* is already taken by an abandoned project.


# Usage

Basic usage:

    from pypiwik.tracker import PiwikTracker
    tracker = PiwikTracker('http://example.com', 1)

now you can call 

    tracker.track_page_view()
    
to make a server-to-server tracking request, or call

    tracker.tracking_code()
    
to generate the correct Javascript snippet.


## Tracking variables

Tracking variables are set as class attributes on the `tracker` object. Have a look at the `pypiwik.tracker.PARAMETERS` dictionary to see which attribute maps to which tracking parameter, e.g.:

    tracker = PiwikTracker('http://example.com', 1)
    tracker.action_name = 'Help / Support'
    tracker.track_page_view()

You can also pass the tracking variables to the `track_page_view` or `tracking_code` call as kwargs. The code above is equivalent to the following:

    tracker = PiwikTracker('http://example.com', 1)
    tracker.track_page_view(action_name='Help / Support')


## Custom variables

Custom variables can be set in the `page_custom_vars` and `visit_custom_vars` dictionary to track custom variables in the `page` and `visit` scope:

_Note:_ Piwik allows at most 5 custom variables per scope. When making server-to-server requests, the code does not check for the numbers of variables in the dictionary.


## Server API

When making server-to-server calls, `pypiwik` will use HTTP headers for the following variables to reduce the request size:

* `user_agent`
* `referer`
* `lang`

If you want to pass the values as regular variables, set `spoof_request` to `False` on the tracker instance.


## Cloning another request

If you want to make server-to-server requests based on a HTTP request of an actual user, pass the request object to `__init__`:

    tracker = PiwikTracker('http://example.com', 1, request)
    
_Note:_ atm, only Django-like request objects supported (an object which has a `META` dictionary).


# TODO

* Implement [Bulk-Tracking](http://developer.piwik.org/api-reference/tracking-api#bulk-tracking)
* Implement the [Ecommerce variables](http://developer.piwik.org/api-reference/tracking-api#optional-ecommercehttppiwikorgdocsecommerce-analytics-info)