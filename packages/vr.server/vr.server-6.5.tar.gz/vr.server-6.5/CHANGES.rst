6.5
---

* Incorporated `project skeleton from jaraco
  <https://github.com/jaraco/skeleton>`_
* Enabled automatic releases of tagged commits
* Tests now run on Travis-CI

6.4.4
-----

* Sort users and apps alphabetically in log page
* Dynamic proc filtering in dashboard

6.4.3
-----

* Fix https://github.com/yougov/velociraptor/issues/208

6.2.0
-----

* Run scooper task every 4 hours by default
* Optimise SQL queries by fetching related entities at once

6.1.0
-----

* Pin `requests` to avoid https://github.com/kennethreitz/requests/issues/3174
* Fix https://bitbucket.org/yougov/velociraptor/issues/165/navigating-back-after-dispatching-a-swarm
* Fix broken images link by not hardcoding static path
* Fix collection of proc names by using the correct line separator character

6.0.0
-----

* When resolving a repository scheme, the default command is now
  ``hg debugexpandscheme``, as that's the official command that
  is included with Mercurial 3.8.

  For compatibility with the previous behavior, set
  ``SCHEME_EXPAND_COMMAND=hg expand-scheme`` in the
  environment.

5.3.0
-----

* #201 Add support for NewRelic

5.0.1
-----

* Additional model garbage collection to troubleshoot memory leak in UI.

5.0.0
-----

* Removed dependency on Flower. Deployments should include
  the Flower dependency in their deployment if they wish
  to provide that service.
