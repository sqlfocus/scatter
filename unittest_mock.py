#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import unittest.mock

'''
unittest.mock is a library for testing in Python. It allows 
you to replace parts of your system under test with mock 
objects and make assertions about how they have been used.
'''
ATTR = "OLD"
def TestFunc():
    pass
class ProductionClass:
    '''
    test class
    '''
    def __init__(self):
        self.attr = "test"
    def method(self):
        return self.method_sub(1, 2, 3)
    def method_sub(self, a, b, c):
        pass
    def closer(self, something):
        something.close()
    
class TestPatch(unittest.TestCase):
    '''
    normal use for 'unittest.mock.patch': used for patching objects
    only within the scope of the function they decorate
    '''
    def test_patch_attr(self):
        #case1: mock class attr by 'patch.object'
        instance = ProductionClass()
        original = instance.attr
        
        @unittest.mock.patch.object(instance, "attr", "new")
        def test():
            self.assertEqual(instance.attr, "new")
        test()
        
        self.assertEqual(original, "test")
        self.assertEqual(original, instance.attr)

        #case2: mock module attr by 'patch'
        @unittest.mock.patch("__main__.ATTR", "NEW")
        def test():
            self.assertEqual(ATTR, "NEW")
        test()
        self.assertEqual(ATTR, "OLD")
    
    def test_patch_method(self):
        #case1: mock module method
        mock = unittest.mock.Mock(return_value=3)
        with unittest.mock.patch('builtins.open', mock):
            handle = open('filename', 'r')
            self.assertEqual(handle, 3)

        #case2: class method as arg
        @unittest.mock.patch.object(ProductionClass, 'method_sub')
        def test_class_mem(patch_method_sub):
            patch_method_sub.return_value = 3   #set return value
            self.assertEqual(ProductionClass().method(), 3)
            patch_method_sub.assert_called_with(1, 2, 3)
        test_class_mem()

        #case3: module method
        @unittest.mock.patch("__main__.TestFunc", return_value="hi")
        def test_module_mem(patch_TestFunc):
            self.assertEqual(TestFunc(), "hi")
            patch_TestFunc.assert_called_with()
            
            patch_TestFunc.return_value = 3   #set return value
            self.assertEqual(TestFunc(), 3)
            patch_TestFunc.assert_called_with()
        test_module_mem()

        #case4: useful for 'setup'/'teardown()'
        config = {'method.return_value': 3, 'other.side_effect': KeyError}
        patcher = unittest.mock.patch('__main__.ProductionClass', **config)
        production_mock = patcher.start()
        self.assertEqual(ProductionClass.method(), 3)
        self.assertEqual(production_mock.method(), 3)
        patcher.stop()
        self.assertEqual(ProductionClass().method(), None)

    def test_patch_class(self):
        #case1: as context
        def some_function():
            instance = ProductionClass()   #call mock()
            return instance.method()       #call mock().method()
        with unittest.mock.patch('__main__.ProductionClass') as mock:
            instance = mock.return_value   #__main__.ProductionClass() <==> mock()
            instance.method.return_value = 101  #return value of 'instance=mock()'.method()
            self.assertIs(instance, ProductionClass())
            self.assertEqual(some_function(), 101)
            
        #case2: as func arg
        @unittest.mock.patch('__main__.ProductionClass')
        def test(mock_class):
            mock_class.method.return_value = 101
            self.assertEqual(mock_class.method(), 101)
            self.assertEqual(ProductionClass.method(), 101)
        test()
        
    def test_patch_dict(self):
        '''
        use patch.dict: can be used to add members to a dictionary, 
        or simply let a test change a dictionary
        '''
        #case1: add new attr
        import os
        with unittest.mock.patch.dict('os.environ', {'newkey': 'newvalue'}):
            self.assertEqual(os.environ.get('newkey', None), 'newvalue')
        self.assertEqual(os.environ.get('newkey', None), None)

        #case2: clear old attr, and add new attr
        foo = {'key': 'value'}
        original = foo.copy()
        with unittest.mock.patch.dict(foo, {'newkey': 'newvalue'}, clear=True):
            self.assertEqual(foo, {'newkey': 'newvalue'})
        self.assertEqual(foo, original)
        

class TestClassMock(unittest.TestCase):
    '''
    normal use for "class mock.Mock/MagicMock"
    '''
    def test_module_attr(self):
        #case1: add attr by "configure_mock"
        mod = unittest.mock.Mock()
        attrs = {'method.return_value': 3, 'other.side_effect': KeyError, 'attr':5}
        mod.configure_mock(**attrs)
        self.assertEqual(mod.method(), 3)
        self.assertRaises(KeyError, mod.other)
        self.assertEqual(mod.attr, 5)

        #case2: add attr as normal module
        mod.attr = 3
        self.assertEqual(mod.attr, 3)

    def test_method_call(self):
        #case1: mock method, specify return value
        real = ProductionClass()
        real.method_sub = unittest.mock.Mock()
        real.method_sub.return_value = 3
        self.assertEqual(real.method(), 3)
        self.assertTrue(real.method_sub.called)
        
        #case2: trace all calls
        real.method_sub.assert_called_once_with(1, 2, 3)
        self.assertEqual(real.method_sub.mock_calls, [unittest.mock.call.method_sub(1, 2, 3)])
        self.assertEqual(real.method_sub.call_args_list, [unittest.mock.call(1, 2, 3)])
        self.assertEqual(real.method_sub.call_args, unittest.mock.call(1, 2, 3))
        self.assertEqual(real.method_sub.call_args[0], (1, 2, 3))

        #case3: trace different args
        mock = unittest.mock.Mock()
        mock(1, 2, 3, k="4")
        self.assertEqual(mock.call_args[0], (1, 2, 3))
        self.assertEqual(mock.call_args[1], {"k" : "4"})

        #case4: mock method, by another func
        vals = {(1, 2, 3): 1, (2, 3, 4): 2}
        def side_effect(*args):
            return vals[args]
        real.method_sub = unittest.mock.Mock(side_effect=side_effect)
        self.assertEqual(real.method(), 1)

        #case5: mock for Method Calls on an Object
        mock = unittest.mock.Mock()
        real.closer(mock)
        mock.close.assert_called_with()
        
    def test_method_ret(self):
        #case1: specify return value by 'return_value'
        real = ProductionClass()
        real.method_sub = unittest.mock.Mock(return_value=3)
        #real.method_sub = unittest.mock.Mock()
        #real.method_sub.return_value = 3
        self.assertEqual(real.method(), 3)
        self.assertTrue(real.method_sub.called)

    def test_method_arg(self):
        #case1: mock obj have same api as which they are replacing
        thing = ProductionClass()
        thing.method = unittest.mock.create_autospec(thing.method, return_value='fishy')
        self.assertEqual(thing.method(), "fishy")
        self.assertRaises(TypeError, thing.method, "wrong arguments")

    def test_cons_iterator(self):
        #case1: use 'side_effect' construct iterator
        mock = unittest.mock.Mock(side_effect=[4, 5, 6])
        self.assertEqual(mock(), 4)
        self.assertEqual(mock(), 5)
        self.assertEqual(mock(), 6)

    def test_exception(self):
        #case1: raise exception use 'side_effect'
        thing = unittest.mock.Mock(side_effect=KeyError('foo'))
        self.assertRaises(KeyError, thing)


if __name__ == '__main__':
    unittest.main(verbosity=2)
