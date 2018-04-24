Flux App v2 Design Documents
============================

Overview
--------

These are some design docs for v2 of the Flux UI and API. Currently the API is hosted on Heroku,
with a MongoDB backend and written as one large python module. It has some scheduled tasks and otherwise
just responds to HTTP / WS.

This has a number of downsides:

* Not open source (basically bc I (Max) am not confident enough that it's high enough quality to open source,
  it has private member details after all)
* Harder to modify due to lack of modularity
* Hard to extricate services or change stuff without breaking things
* DB is badly architected - one big user object for example

There's a strong need to do something about this before we get too much tech debt. Especially because
it's not extensible and I (Max) am the only dev currently which does not scale.

This document concerns the replacement of _all_ features of the v1 api. They'll be listed and described
below, as well as ideas on how to build a better api and what new features would be good to introduce.

Other relevant docs:

* `Membership UI v2 notes on
  GitHub <https://github.com/voteflux/flux-tech-roadmap/blob/master/MembershipUI-v2.md>`_
* `Flux Tech Roadmap issues <https://github.com/voteflux/flux-tech-roadmap/issues>`_
  (has a bunch of discussion about forum, migrations, docs, cms, etc)
* `Old flux app code from 2016 - never used <https://github.com/XertroV/flux-app>`_
  (mostly if you're curious)

Broadly speaking, these features include:

* Admin functionality

  - Sending transactional emails and SMSs
  - Viewing member details and minor administration
  - Validating members (note: preference to build publicly accessible validation tools where possible)
  - Granting roles and permissions
  - Generating membership lists (for rego and communication)
  - Potentially doing phone banking
  - Possibly auto-managing email addresses, branches, etc (not in v1)
  - CMS / content / blog posts (not in v1)
  - Email mailing lists (not in v1 - using mailchimp)
  - Email UI? (not in v1 and maybe not a great idea - but would allow us to move away from Google Apps which
    are a bit expensive)
  - Manage steerco meetings / minutes / calander invites / etc - can auto publish minutes / sections of minutes
    (not in v1 but I'd actually really like to see something like this formalised)

* Membership functionality

  - signup (note: also enforces address standards that allow for MUCH better validation - we DO NOT want to take
    arbitrary addresses, that's just asking for pain)
  - modifying details / preferences
  - credential / access reset (new membership link)
  - doing anonymous validation of other members
  - self validation (not in v1)
  - organising in groups (not in v1)
  - forum access (not in v1)
  - other stuff? (not in v1)
  - membership revocation

Frontend
--------

The idea for the frontend is that we want a unified portal for _all_ membership functionality (including admin).

We also want to support _both_ mobile, desktop, and app packaging from one codebase.

For that reason it seems best to go with common JS based UI tools to create SPAs. This will allow us to build
the UI easily (using CI and then auto-host it. note: we do this now), and also means we can maximise potential
contributors.

It's important to create something that's modular enough we can extend it without worrying about breaking other
things, but also robust enough to go the distance. Ideally we should be doing *as much as possible* through the
UI. This allows us to maximise automation and reuse of common functions (instead of managing things in
spreadsheets or whatever).

Basic UI Description
~~~~~~~~~~~~~~~~~~~~

This is an incomplete and very sketchy overview of the UI / UI flow / features / etc:

* Opening page (login or register)

**Registration**

  * Registration: put in details, submit to api, show thankyou, and then show dashboard
  * See `the current rego page <https://voteflux.org/signup>`_
  * Note: the order of the address (country, postcode, suburb, etc) is deliberate as it allows us to prefil
    feilds with only valid possibilities - we want to maintain that as much as possible and ideally extend it
    to other countries as it becomes available
  * User should get a welcome email and instructions on logging in and the like

**Login**

  * Ideally we do login via a link - this way we can avoid holding usernames and passwords. While offloading
    authentication to email is NOT ideal, it reduces attack vectors on backend. Also ppl are _really_ bad with
    passwords (if you're not using a password manager... well you should be, there's like no good reason not to)
  * either way, keep the login simple, then go to dashbaord

**Member UI**

* Dashboard:

  * for the moment it'll be sparse for users (since there's not much to do)
  * show whether details are valid or not, invite them to self-validate if needed
  * show current details (though not DOB, keep that hidden by default, maybe have a "show dob" button - like we
    want to show we're thinking about privacy stuff)
  * overview of branch stuff, not as detailed as branch page
  * get involved call to action - opens up dialog with branch steerco
  * maybe show more general member stats too

* Edit Details:

  * `current ui <https://api.voteflux.org/static/html/member_details.html>`_
  * place to edit current details - bonus if we can reuse elements from the signup form (note: no reason we
    shouldn't be able to do that). this screen isn't on the main dashboard, but links to it

* Branch Page:

  * view branch info (e.g. who is currently involved, public email contact deets, etc)

* (Future): Forum

  * best idea so far for the forum is to use some kind of api layer over github issues
  * this means we host nothing besides the general API
  * we can use a bot to post to the issues on behalf of users so they don't need to login
    with github details
  * also means we can use some custom markup to indicate which member was posting, etc, without
    necessarily showing their name. We can do some anonymisation and stuff as well if we like
  * also means anyone not in flux can still participate by just posting to issues directly

* (Future): Local groups

  * idea is to have some sort of less-than-steerco local group stuff, e.g. meetups, branch formation, etc
  * allow users to add themselves to local mailing lists, etc

**Admin UI**

* General notes

  * (more technical than member ui - don't focus on ux so much, more about those features)
  * idea: show areas based on roles / permissions
  * all sections should be locked down via branch level permissions - e.g. NSW steerco can't send email to
    VIC members, etc

* Dashboard

  * overview of anything going on with branches that user is involved in (e.g. upcoming meetings, recent
    minutes)
  * election countdown
  * branch stats

* Branch Members

  * allows selecting branch and then viewing members (note: maybe branch should be selected in tab-bar at
    the top or something, remember some ppl are involved in multiple branches)
  * (note: API shouldn't return sensetive info, this is more for finding ppl
    and getting contact info, that sort of thing)

* Communications:

  * Send transactional email (like regarding specific things for those members, e.g. being on a rego list)
  * Send newsletters / other mass email (mailing-list stuff)
  * Other?

* Election Planning

  * Todo

* Finances

  * Issue receipts
  * Log donations (tied to receitps)
  * Maybe enable some kind of payments API (e.g. via cryptocurrency, or something, not really sure but
    would be nice bc then we could control permissions easily)

* Other stuff?

Backend
-------

The backend needs a few key features, but otherwise should essentially be created to support the UI (so
I won't repeat features here)

Authentication
~~~~~~~~~~~~~~

* Idea: use JWTs to handle all authentication - can be long lasting, allow for multi-user stuff if we
  need, safely storable in local storage, easily revocable
* Users get sent a one-time-use token to email with a link, that link mints and delivers a JWT with like
  a 3 month expiry or something (admin JWTs can be enforced to be much shorter)
* Also allows for other microservices to interact with JWTs (allows for addons, essentially)
* Also let's us build in versioning and scalable architecture

Architecture
~~~~~~~~~~~~

Best idea so far (I think) is to use lambda functions for pretty much everything. Makes it super easy to do
drive by contribution, and also really flexible when it comes to AWS stuff / permissions / etc. See `Tech Stack`_.

Integrations
~~~~~~~~~~~~

Current integrations are with:

* Mailchimp
* SMS Gateway and Wholesale SMS (both just simple POST requests)
* PhantomJS / Selenium for validation proxy (note: using lambda or maybe a docker thing here would be
  super useful because
  then we don't have to run it on the main server, which has lead to problems before due to phantomjs memory and
  cpu usage)
* Paypal - we get notifications when ppl send us money, but they've been crap replying to our support emails
  (as we're locked out atm) and they went and changed their donation page so it's not possible to require
  an address anymore - this unfortunately gives an error 500 on the backend atm

Things we might want to integrate with in future

* Google Apps (for email / email-list management)
* Github (forums maybe, issue tracking, posting stuff, pulling things, even like CMS or something)
* AWS services (note, using lambda makes this super easy)

Backwards Compatibility
~~~~~~~~~~~~~~~~~~~~~~~

Ideally we'll build out the new features to be somewhat backwards compatible with the existing DB (we can
connect to it directly). This way we can server data through the new API and then incrementally build up
to v2. We could also just fwd requests we recieve to the old API if need be (e.g. bc we haven't implemented
the v2 version of whatever feature).

Currently there's no good docs on the api, though there are some out of date docs.

Access to the source code (in python) is available for anyone who needs it while developing v2.

The idea here is that if we create the v2 layer that can either proxy stuff to v1 or pull it directly we can
start building the new UI without worrying what goes on behind the scenes in v2. That way we can build everything
out we need to and then do a mass migration to move user details and things across to v2 all at once and do the
switch over. (An easy way to do this is to always check a flag in a ``system`` table or something)

Tech Stack
----------

An early idea is to build primarily on AWS. This has a number of advantages:

- Many services we need - Lambda for API, Static hosting through S3, Build / CI / CD tools, Email sending, etc
- Might be able to get some promo credit
- Even if we don't AWS can be pretty cheap with free tiers + intelligent use of services
- Can be made super modular

We might build on something else though.

Max's preference is for a NoSQL db - though if we use an ORM then SQL could work too (though migrations can
be super annoying)
