================================================
collective.twittercards
================================================
Integrate `Twitter Cards <https://dev.twitter.com/cards/overview>`_ to Plone.

Prerequiresites
================================================
- Plone 4 (tested with Plone >= 4.3.x)

Supported card types
================================================
- Summary Card
- Summary Large Image Card
- Photo Card

Roadmap
================================================
Some of the upcoming/in-development features/improvements are:

- All card types (Summary Card with Large Image, Photo Card,
  Gallery Card, App Card, Player Card, Product Card).
- Per content item configurable twitter cards.

Installation
================================================
Buildout
------------------------------------------------
>>> [instance]
>>> eggs +=
>>>     collective.twittercards

ZMI
------------------------------------------------
ZMI -> portal_quickinstaller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First make sure you have the `collective.z3cform.datagridfield` installed.
- Then choose "collective.twittercards" and install it.

Configuration options
================================================
App control panel can be accessed at
http://your-plone-site.com/@@twittercards-settings

.. figure:: https://github.com/collective/collective.twittercards/raw/master/docs/_static/01_control_panel.png
    :align: center

Contributors
============

Note:  place names and roles of the people who contribute to this package
       in this file, one to a line, like so:

- Kenneth Veldman, Original Author
- Peter Uittenbroek, valuables improvements/fixes.
- Artur Barseghyan, documentation and packaging improvements.


Changelog
=========
0.1.3 (2015-03-03)
--------------------

- Added support for Summary Large Image and Photo Cards.

0.1.2 (2015-02-03)
--------------------

- Documentation added.

0.1.1 (2015-02-02)
--------------------

- Added twitter viewlet and various settings to be able to select what type of
  card should be used for a certain content type.

0.1 (2015-01-30)
--------------------

- Initial release.


