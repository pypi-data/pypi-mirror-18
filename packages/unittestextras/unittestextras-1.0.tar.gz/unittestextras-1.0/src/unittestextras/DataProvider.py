__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '11/21/16'
__doc__ = """
based on solution provided at: http://stackoverflow.com/questions/2798956/python-unittest-generate-multiple-tests-programmatically
"""

import sys


def DataProvider(data_set, id_key=None, id_index=None):
  """
  Data provider decorator, allows another callable to provide the data for the test

  :param data_set: a DataSet instance that can provide sets of data as expected by the test method decorated
  :param id_key: optional key to use for reporting failures
  :param id_index: optional index of argument to use for reporting failures
  """
  def test_decorator(test_method, parameters=data_set):
    for parameter in parameters():
      if isinstance(parameter, dict):
        args_for_parameter = str(parameter[id_key]) if id_key is not None else str(parameter[id_index]) if id_index is not None else ",".join('%s=%s' % (k,v) for k,v in parameter.iteritems())
        def decorated(self, method=test_method, parameter=parameter):
          method(self, **parameter)
      else:
        parameter = parameter if isinstance(parameter, (list, tuple)) else (parameter, )
        args_for_parameter = str(parameter[id_index]) if id_index is not None else ",".join(repr(v) for v in parameter)
        def decorated(self, method=test_method, parameter=parameter):
          method(self, *parameter)

      name_for_parameter = test_method.__name__ + "(" + args_for_parameter + ")"
      for i in range(10):
        try:
          x = sys._getframe(i).f_locals
        except:
          break
      frame = sys._getframe(1)  # pylint: disable-msg=W0212
      frame.f_locals[name_for_parameter] = decorated
    return None
  return test_decorator