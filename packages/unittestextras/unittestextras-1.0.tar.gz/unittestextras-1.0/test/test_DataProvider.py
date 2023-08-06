__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '11/21/16'

from unittest import TestCase, TestLoader, TextTestRunner, TestSuite
from src.unittestextras import DataSet, DataProvider
from StringIO import StringIO


class test_DataProvider(TestCase):
  setup_count = 0
  teardown_count = 0

  class DataProviderInner(TestCase):
    """
    """
    data_dict = DataSet(
      dict(x=10, y=20, label='set a'),
      dict(x=5, y=7, label='set b'),
      dict(x=100, y=5, label='set c'),
      dict(x=100, y="st", label='set d')
    )

    data_list = DataSet(
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
      [4, 4, 0]
    )

    data_strings = DataSet(
      "string_2",
      1,
      0.5,
      ((1, 2, 3), )
    )

    @DataProvider(data_list)
    def test_me_list(self, x=1, y=1, z=1):
      print self.id(), x
      induce_divided_by_zero_error = x/z
      self.assertEquals(x+y, z)

    @DataProvider(data_list, id_index=2)
    def test_me_l_indexed(self, x=1, y=1, z=1):
      print self.id(), x
      induce_divided_by_zero_error = x/z
      self.assertEquals(x+y, z)

    @DataProvider(data_dict)
    def test_me_dict(self, x=1, y=1, z=1, label=None):
      print self.id(), x
      if type(x) != type(y): raise StandardError("not same type")
      self.assertGreater(x, y)

    @DataProvider(data_dict, id_key='y')
    def test_me_d_key(self, x=1, y=1, z=1, label=None):
      print self.id(), x
      if type(x) != type(y): raise StandardError("not same type")
      self.assertGreater(x, y)


    @DataProvider(data_strings)
    def test_me_primitives(self, x=1, y=1, z=1):
      print self.id(), x
      if isinstance(x, tuple):
        import InduceImportError
      self.assertIsInstance(x, str)

    def setUp(self):
      test_DataProvider.setup_count += 1

    def tearDown(self):
      test_DataProvider.teardown_count += 1


  def setUp(self):
    self.__class__.teardown_count = 0
    self.__class__.setup_count = 0
    self.suite = TestLoader().loadTestsFromTestCase(self.DataProviderInner)

  def tearDown(self):
    pass

  def _subsuite(self, suite, pattern):
    subsuite = TestSuite()
    for test in suite:
      if pattern in test._testMethodName:
        subsuite.addTest(test)
    return subsuite

  def test_provided_primitives(self):
    self.assertEqual(self.setup_count, 0)
    self.assertEqual(self.teardown_count, 0)
    results = TextTestRunner(stream=StringIO()).run(self._subsuite(self.suite, 'primitive'))
    print results
    self.assertEqual(self.setup_count, 4)
    self.assertEqual(self.teardown_count, 4)
    self.assertEqual(results.testsRun, 4)
    self.assertEqual(len(results.failures), 2)
    self.assertEqual(len(results.errors), 1)

  def test_provided_list(self):
    self.assertEqual(self.setup_count, 0)
    self.assertEqual(self.teardown_count, 0)
    results = TextTestRunner(stream=StringIO()).run(self._subsuite(self.suite, 'list'))
    print results
    self.assertEqual(self.setup_count, 4)
    self.assertEqual(self.teardown_count, 4)
    self.assertEqual(results.testsRun, 4)
    self.assertEqual(len(results.failures), 2)
    self.assertEqual(len(results.errors), 1)

  def test_provided_list_indexed(self):
    self.assertEqual(self.setup_count, 0)
    self.assertEqual(self.teardown_count, 0)
    results = TextTestRunner(stream=StringIO()).run(self._subsuite(self.suite, 'l_index'))
    print results
    self.assertEqual(self.setup_count, 4)
    self.assertEqual(self.teardown_count, 4)
    self.assertEqual(results.testsRun, 4)
    self.assertEqual(len(results.failures), 2)
    self.assertEqual(len(results.errors), 1)

  def test_provided_dict(self):
    self.assertEqual(self.setup_count, 0)
    self.assertEqual(self.teardown_count, 0)
    results = TextTestRunner(stream=StringIO()).run(self._subsuite(self.suite, 'dict'))
    print results
    self.assertEqual(self.setup_count, 4)
    self.assertEqual(self.teardown_count, 4)
    self.assertEqual(results.testsRun, 4)
    self.assertEqual(len(results.failures), 2)
    self.assertEqual(len(results.errors), 1)

  def test_provided_dict_keyed(self):
    self.assertEqual(self.setup_count, 0)
    self.assertEqual(self.teardown_count, 0)
    results = TextTestRunner(stream=StringIO()).run(self._subsuite(self.suite, 'd_key'))
    print results
    self.assertEqual(self.setup_count, 4)
    self.assertEqual(self.teardown_count, 4)
    self.assertEqual(results.testsRun, 4)
    self.assertEqual(len(results.failures), 2)
    self.assertEqual(len(results.errors), 1)
