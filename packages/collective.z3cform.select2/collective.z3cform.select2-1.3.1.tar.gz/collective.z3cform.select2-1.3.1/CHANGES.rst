Changelog
=========


1.3.1 (2016-12-09)
------------------

- Rename wrong class facted-select-criterion to faceted-select-criterion
  [vincentfretin]


1.3 (2016-12-01)
----------------

- Remove specific css rules that was introduced in 1.2
  [vincentfretin]

- Fix widget in overlays. If you upgrade from 1.1, you need to reinstall
  the profile to add a css in portal_css.
  [cedricmessiant]

- Wrap call to select2 initialization in JS function `initializeSelect2Widgets`
  so it is easy to call from everywhere (like in an overlay initialization).
  Parameter width can be specified when calling `initializeSelect2Widgets`
  and defaults to `resolve`.
  [gbastien]


1.2 (2016-08-25)
----------------

- Avoid an error if Faceted namespace is not defined
  [mpeeters]

- Add a select2 single and multi select widget
  [mpeeters]


1.1 (2016-07-07)
----------------

- Use faceted-select2-widget instead of faceted-select-widget to not break
  the original faceted-select-widget widget.
  [vincentfretin]

- Depends on eea.jquery >= 8.8 to fix images in select2.
  [vincentfretin]

- Replace collective.taxonomy.widget.TaxonomySelectFieldWidget by the widget
  from this package.
  [vincentfretin]

- Initialize widgets in overlays now.
  [vincentfretin]


1.0 (2016-04-20)
----------------

- Initial release.
  [vincentfretin]
