*********
Gladiator
*********

Validation Framework for Python3


A quick example
===============

A registration form accepts this data structure::

  valid_test_data = {
      'email': 'test@example.com',
      'pw': 'password123',
      'name': 'Test Username',
      'birth_year': 1984
  }


The validation process can be::

  import gladiator as gl
  
  registration_form_validator = (
      ('email', gl.required, gl.format_email),
      ('pw', gl.required, gl.length_min(5)),
      ('name', gl.required, gl.type_(str)),
      ('birth_year', gl.required, gl.type_(int), gl.value_max(2014 - 18))
  )
  
  result = gl.validate(registration_form_validator, valid_test_data)
  assert result.success is True


