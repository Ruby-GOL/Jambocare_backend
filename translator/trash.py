Internal Server Error: /translator/record/
Traceback (most recent call last):
  File "C:\Users\Administrator\.virtualenvs\Jambocare_backend-QogWEPzZ\Lib\site-packages\django\core\handlers\exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Administrator\.virtualenvs\Jambocare_backend-QogWEPzZ\Lib\site-packages\django\core\handlers\base.py", line 220, in _get_response
    response = response.render()
               ^^^^^^^^^^^^^^^^^
  File "C:\Users\Administrator\.virtualenvs\Jambocare_backend-QogWEPzZ\Lib\site-packages\django\template\response.py", line 114, in render
    self.content = self.rendered_content
                   ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Administrator\.virtualenvs\Jambocare_backend-QogWEPzZ\Lib\site-packages\rest_framework\response.py", line 70, in rendered_content
    ret = renderer.render(self.data, accepted_media_type, context)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Administrator\.virtualenvs\Jambocare_backend-QogWEPzZ\Lib\site-packages\rest_framework\renderers.py", line 99, in render
    ret = json.dumps(
          ^^^^^^^^^^^
  File "C:\Users\Administrator\.virtualenvs\Jambocare_backend-QogWEPzZ\Lib\site-packages\rest_framework\utils\json.py", line 25, in dumps
    return json.dumps(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\json\__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "C:\Python311\Lib\json\encoder.py", line 200, in encode
    chunks = self.iterencode(o, _one_shot=True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\json\encoder.py", line 258, in iterencode
    return _iterencode(o, 0)
           ^^^^^^^^^^^^^^^^^
  File "C:\Users\Administrator\.virtualenvs\Jambocare_backend-QogWEPzZ\Lib\site-packages\rest_framework\utils\encoders.py", line 50, in default
    return obj.decode()
           ^^^^^^^^^^^^
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5 in position 5: invalid continuation byte