# BitlyOAuth2ProxySession

This is a simple subclass of `requests.Session` which, when initialized,
or when you call its `authenticate()` method, does the magic to talk to
the Bitly OAuth2 Proxy and return a session that is authenticated for
whatever is behind it.

The use case here is a read-only service user, which does not require
two-factor authentication, that you want to be able to access resources
behind the Bitly proxy.  Our _particular_ use case right now is for a
monitoring system to be able to check on web pages that require
authentication.  There's one class, the imaginatively-named `Session`.

## Installation

`pip install bitly-oauth2-proxy-session`

Or check out the repository, `cd` to its root directory, and `python
setup.py install`.  It requires a fairly recent `requests` (2.8.1 or
later).

## Instance Attributes

* `oauth2_username`: a string containing the username of the underlying
  OAuth2 user.
* `oauth2_password`: a string containing the password of the underlying
  OAuth2 user.  At least for GitHub, you can't use an auth token.  The
  reason behind this seems to be that this is what you'd do if you were
  an actual user with an actual web browser.  Yes, this means 2FA isn't
  currently supported.
* `authentication_base_url`: a string containing the `start` URL of your
  oauth proxy.  Typically, _site_`/oauth2/start`.
* `authentication_session_url`: a string containing the URL of the page
  you POST to when you create a session with the underlying OAuth2
  source as a web user.  For Github, this is
  `https://github.com/session` and that's the default.
* `authentication_postdata`: a Python dict containing the data you need
  to POST to the session URL.  Defaults to the right thing for Github.

## Methods

* `[get_/set_]*()`: getters and setters for the various instance
  attributes.  No, you can't get the password this way.
* `authenticate()`: run the authentication dance and store the magic in
  the session object.

## Usage

* Acquire a `Session` object.
  * For Github, create the object with `oauth2_username`,
    `oauth2_password`, and `authentication_session_url`.
  * For something else (untested), create the object empty, set all the
    fields via the setter methods, and then run `authenticate()`.  Pull
    requests welcomed.
* Do sessiony things, like `get()` and `post()`.

## Bugs

* If anyone knows how I can get a session with a Github user token
  rather than a password, that'd be great.
* Github is the only working use case right now.




