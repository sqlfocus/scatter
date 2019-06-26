#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest


def setUpModule():
    '''before any test case'''
    pass

def tearDownModule():
    '''after any test case'''
    pass


@unittest.skip("class skipping")
class TestSkip(unittest.TestCase):
    '''
    testclass or testcase can be skip
    '''
    #@unittest.skip("demonstrating skipping")
    #@unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    #@unittest.skipIf(1<3, "condition that skip")
    def test_nothing(self):
        '''Skipping a test'''
        if not False:
            self.skipTest("resource not available")

        self.fail("shouldn't happen")

        
class TestExpectedFailure(unittest.TestCase):
    '''
    expected failure
    '''
    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")

        
def _do_without_args():
    raise BlockingIOError
def _do_with_args(a, b, c):
    raise BlockingIOError
class TestRaiseExcep(unittest.TestCase):
    '''
    raise exception
    '''
    def test_raise(self):
        ###case1
        #cm.exception store the exception instance
        with self.assertRaises(BlockingIOError) as cm:
            _do_without_args()
        self.assertIsInstance(cm.exception, BlockingIOError)

        ###case2
        self.assertRaises(BlockingIOError, _do_with_args, 1, "2", None)

        
class TestLog(unittest.TestCase):
    '''
    test logger output
    '''
    def test_log(self):
        with self.assertLogs('foo', level='INFO') as cm:
            logging.getLogger('foo').info('first message')
            logging.getLogger('foo.bar').error('second message')
            
        self.assertEqual(cm.output, ['INFO:foo:first message',
                                     'ERROR:foo.bar:second message'])
        
###individual unit of testing
class TestStringMethods(unittest.TestCase):
    '''
    test case by ourself
     1. name begin by "Test"
     2. parent "unittest.TestCase"

    <NOTE>
     1. assertEqual/assertNotEqual(): check for an expected result
     2. assertDictEqual/assertSetEqual/assertListEqual/assertTupleEqual()
     3. assertIn/assertNotIn(): check a is in or not in b
     4. assertIs/assertIsNot(): check two obj is the same one
     5. assertIsInstance/assertNotIsInstance()
     6. assertIsNone/assertIsNotNone()
     7. assertLess/assertLessEqual/assertGreater/assertGreaterEqual()
     8. assertTrue/assertFalse(): verify a condition
     9. assertRaises(): verify specific exception gets raised
    '''
    @classmethod
    def setUpClass(cls):
        '''executed before any test method'''
        pass
    def setUp(self):
        '''executed before each test method'''
        pass
    
    @classmethod
    def tearDownClass(cls):
        '''executed after any test method'''
        pass
    def tearDown(self):
        '''executed after each test method'''
        pass


    def test_upper(self):
        '''
        one special test case
         1. name begin by "test"
        '''
        self.assertEqual('foo'.upper(), 'FOO', "upper() failed")

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


###create test suit
def suite():
    tmp = unittest.TestSuite()

    ###case1: add test case
    #tmp.addTests(unittest.TestLoader().loadTestsFromNames([
    #    'unittest_template.TestSkip',
    #    'unittest_template.TestExpectedFailure',
    #    'unittest_template.TestRaiseExcep',
    #    'unittest_template.TestLog',
    #    'unittest_template.TestStringMethods'
    #]))

    ###case2: add test func
    tmp.addTest(TestSkip('test_nothing'))
    tmp.addTest(TestExpectedFailure('test_fail'))
    tmp.addTest(TestRaiseExcep('test_raise'))
    tmp.addTest(TestLog('test_log'))
    tmp.addTest(TestStringMethods('test_upper'))
    tmp.addTest(TestStringMethods('test_isupper'))
    
    return tmp

###main
if __name__ == '__main__':
    '''
    0. 执行本文件   python unittest_template.py
    1. 执行某个模块的单元测试 python -m unittest unittest_template
    2. 执行某个测试类 python -m unittest unittest_template.TestStringMethods
    3. 执行某测试函数 python -m unittest unittest_template.TestStringMethods.test_isupper
    4. 模块、测试类、测试函数可以任意组合传入 python -m unittest ...
    5. 通过文件路径制定模块   python -m unittest tests/test_something.py
    6. 现实详细信息 python -m unittest -v unittest_template
    7. 查看帮助信息 python -m unittest -h
    '''
    ###方式1:
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
    
    ###方式2:
    #unittest.main(verbosity=2)


