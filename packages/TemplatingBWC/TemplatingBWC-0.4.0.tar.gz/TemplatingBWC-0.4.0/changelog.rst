Change Log
----------


0.4.0 released 2016-11-29
===========================

* Add support for Python 3 (3.4 and 3.5)
* Set up continuous integration testing on CircleCI and AppVeyor
* Test coverage is on CodeCov

0.3.1 released 2014-09-18
===========================

* BC break: updated jQuery to latest 1.x version (1.11.1)
* updates related to jQuery: jQuery-UI, Superfish, HoverIntent
* jQuery-UI css now monolithic, jquery_ui_links macro deprecated
* Select2 updated to 3.5.1
* removed webgrid-specific CSS (relevant styles are in webgrid)
* updated image-link text-indents which would be problematic for wide displays

0.3.0 released 2014-08-20
===========================

* adding Select2 UI element
* updating jquery libs while maintaining compatibility with older UI elements
  such as Multiselect
* add "head_end" to admin template for easily adding tags to end of HTML head


0.2.1/2 released 2014-07-14
===========================

* fixed submit button left margin on admin template forms.  Was 110px but needed
  to be 160px to match the label + margin.
* add css to make cancel buttons look like a link
