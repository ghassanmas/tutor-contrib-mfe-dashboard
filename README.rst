Tutor plugin to enable learner dashboard MFE for `Tutor <https://docs.tutor.overhang.io>`__
===========================================================================================


**Note**: This is not maintained, please use this plugin instead https://github.com/openedx/openedx-tutor-plugins/tree/main/plugins/tutor-contrib-learner-dashboard-mfe 

Overview
--------

This plugins allows you to use `frontend-app-learner-dashboard <https://github.com/openedx/frontend-app-learner-dashboard>`__. 
Currenlty it points to my fork, it needs some changes to work with tutor, which are still not merged upstream. `Ref PR <https://github.com/openedx/frontend-app-learner-dashboard/pull/136>`__.

The dashbaord MFE is expected to be included as **experimental** in `Open edX Palm release <https://github.com/openedx/docs.openedx.org/pull/321>`__. 

Installation
------------

::

    pip install git+https://github.com/ghassanmas/tutor-contrib-mfe-dashboard

Usage
-----

::

    tutor plugins enable dashboard
    tutor config save 
    tutor local do init --limit=dashboard
    tutor images build mfe 
    tutor local start mfe -d 


Disable 
-------
 
Note that ``tutor local do init --limit=dashbaord`` creates two waffle toggle so we need to delete/deactivate them.

:: 

    tutor local run lms ./manage.py lms waffle_flag --deactivate learner_home_mfe.enabled
    tutor local run lms ./manage.py lms waffle_flag --decativate --everyone learner_recommendations.enable_dashboard_recommendations
    tutor plugins disable dashbaord
    tutor config save 
    tutor local restart mfe 

Note: You could rebuild the tutor-mfe image, but that is unnecessary. It would save you about ~20MB. 


License
-------

This software is licensed under the terms of the AGPLv3.
