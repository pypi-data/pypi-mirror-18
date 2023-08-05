1.0.5
-----

- *BUGFIX*: Manifest fix

1.0.4
-----

- *UPDATE*: Switched the user pagination to use 25 rows
- *BUGFIX*: Fixed two small bugs with pagination

1.0.3
-----

- *BUGFIX*: The pywebtools.pyramid.util.paginate function now takes the route_name for URL generation
- *BUGFIX*: The pywebtools.pyramid.auth.views.users function now generates the pagination before limiting the query

1.0.2

- *NEW*: Added py.test fixtures

1.0.1
-----

- *BUGFIX*: Fixed missing Kajiki files

1.0.0
-----

- *NEW*: Complete, incompatible re-write of the package

0.5.2
-----

- *BUGFIX*: Use the request.response object to allow view code to modify the response

0.5.1
-----

- *BUGFIX*: Don't force a unicode conversion when outputting CSV files

0.5
-----

- *NEW*: assert_authorised raises an auth.AccessDeniedException if the authorisation statement does not hold
  
0.4.2
-----

- *UPDATE*: Ignore extra columns when writing CSV files

0.4.1
-----

- *BUGFIX*: Fixed the way the request is identified in the Genshi renderer

0.4
---

- *UPDATE*: pywebtools.renderer template defaults are now set per content type

0.3
---

- *NEW*: pywebtools.renderer module for integrating Genshi with the Pyramid framework

0.2.1
-----

- *BUGFIX*: Generate the right field type for form.text_field

0.2
---

- *UPDATE*: Added pywebtools.form.radio for generating radio buttons.

0.1
---

- *NEW*: Initial version
