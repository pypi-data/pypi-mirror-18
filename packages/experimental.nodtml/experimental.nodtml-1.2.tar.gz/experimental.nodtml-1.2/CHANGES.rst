Changelog
=========


1.2 (2016-11-14)
----------------

New features:

- Added ``EXPERIMENTAL_NODTML_RAISE`` option.  [maurits]


1.1 (2016-09-28)
----------------

New features:

- Added ``EXPERIMENTAL_NODTML_ONLY_WARN`` option.  [maurits]

Bug fixes:

- Interpret value of ``SHOW_ORIGINAL_DTML`` as true value.
  Accepted True values are: ``true``, ``t``, ``1``, ``yes``, ``y``.
  [maurits]

- Show arguments and keyword arguments when ``SHOW_ORIGINAL_DTML`` is true.
  [maurits]

- Return empty string instead of empty unicode by default.  Otherwise
  you get exceptions when loading dtml files in for example the css
  registry on Plone 4.3.  [maurits]


1.0.2 (2016-09-24)
------------------

Bug fixes:

- Fixed showing ``String .__str__``.  [maurits]


1.0.1 (2016-09-24)
------------------

Bug fixes:

- Added z3c.autoinclude entry point, so our code gets loaded on startup.  [maurits]


1.0 (2016-09-24)
----------------

- Initial release.
  [mauritsvanrees]
