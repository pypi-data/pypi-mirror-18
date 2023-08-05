Change Log for farmdrop
====================================

Dev
---

  * Move template context processors to their rightful plcae
  * Combine rules in the makefile and add dep link to setup
  * Requisite fixing the MANIFEST file commit


2.3.3
-----

  * Fixing init file ... again
  * Just kidding, now we've got the make file fixed


2.3.2
-----

  * Adding proper init file stuffs back in and fixing borked makefile


2.3.1
-----

  * Fix few issues of templates not working
  * Fix for celery task queue
  * Adding better default media bucket path and fixing template bug


2.3.0
-----

  * Improving search


2.2.1
-----

  * Build not just blank for pcakaging in the Makefile
  * We want to use base dir, not public for whoosh index


2.2.0
-----

  * Adding haystack to apps
  * Adding twitter sharing buttons
  * Making the CELERY QUEUE modifyable


2.1.0
-----

  * Update the Makefile packaging scripts
  * Add search indexing for sermons and fixing BROKER settings for SQS
  * Tack a dev version on our next minor version
  * Adding utils and pubic folder configuration options
  * Adding make file commands for distribution


2.0.0
-----

  * Remove honcho from the project requirements
  * Fix honcho requirement
  * Fix file permissions on download tasks
  * Fixing unicode issues and featureing
  * Fix broker queue settings
  * Fixing tasks for delivering and sending
  * Make zip_single task easier to test
  * Update farmdrop version number
  * Update worker procfile and remove logging bug from downloads
  * Update version to 2 alpha 1
  * Removing the env file and adding Proc and example env file
  * Fixing celery tasky goodness
  * Cleaning up migrations and database
  * Fixing endless pagination and downloads
  * Add celery file and update settings
  * Adding reqs needed for filer and forms_builder
  * Updating setup requirements and adding mptt to codebase
  * Move to better template tag that doesn't barf on non-existing pages
  * Adding migrations
  * Updating templates for django 1.9
  * Big shuffle for py3
  * Initial commit

