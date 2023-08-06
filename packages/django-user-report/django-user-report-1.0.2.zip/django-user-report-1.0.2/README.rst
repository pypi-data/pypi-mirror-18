=====
User Content Report System
=====

IOS apps may may require server side has a report system to ensure each content user created can be reporeted and removed. This small django app comes with those essential features that you don't have to implement yourself:

1. Query, monitor all tickets users sent from front-end app on Django Admin Page.
2. Admin can set priorities, delete content, banning users directly on the admin page. 
3. Built in REST api for front-end calling and sumbitting a ticket.
4. By default, enabled Email notification to target User (content creator).

Quick start
-----------

1. Add "report_system" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'report_system',
    ]

2. Configure Those settings (Recommended)::

    # REPORT SYSTEM
	REPORT_SLUG_MODEL_MAPPINGS = (
	    ('user', AUTH_USER_MODEL),
	    ('user_blog', 'blogs.blog'),
	    ...
	)
	REPORT_EMAIL_RECEIVER_FIELDNAME = (
	    (AUTH_USER_MODEL, None),
	    ('blogs.blog', 'author'),
	)
	REPORT_EMAIL_FROM = DEFAULT_FROM_EMAIL

3. Run `python manage.py migrate` to create the Report System Tickets models.
