#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging

import asynctest

'''
refer https://github.com/Martiusweb/asynctest
- install: pip install asynctest
- run: python3 -m unittest unittest_asynctest.py
'''

class MinimalExample(asynctest.TestCase):
    '''
    CAN used to construct normal unittest case,
    because asynctest just inherit from unittest
    and create more feature
    '''
    def test_that_true_is_true(self):
        self.assertTrue(True)

        
class AnExampleWithSetup(asynctest.TestCase):
    '''
    create a loop by ourself, run test case, 
    and clear it
    '''
    async def a_coroutine(self):
        return "I worked"

    def setUp(self):
        self.my_loop = asyncio.new_event_loop()
        #self.addCleanup(self.my_loop.close)      #same as 'tearDown()'
    def tearDown(self):
        self.my_loop.close()
        
    def test_that_a_coroutine_runs(self):
        result = self.my_loop.run_until_complete(self.a_coroutine())
        self.assertIn("worked", result)

class AnExampleWithTestCaseLoop(asynctest.TestCase):
    '''
    asynctest.TestCase will create (and clean) an event loop
    for each test that will run. This loop is set in the loop
    attribute
    '''
    async def a_coroutine(self):
        return "I worked"

    def test_that_a_coroutine_runs(self):
        result = self.loop.run_until_complete(self.a_coroutine())
        self.assertIn("worked", result)

    async def test_that_a_coroutine_runs_2(self):
        '''
        tests functions can be coroutines
        '''
        self.assertIn("worked", await self.a_coroutine())
    
##############################mock############################
import asynctest.mock

class Client:
    '''
    sync client
    '''
    def add_user(self, user):
        raise NotImplementedError

    def get_users(self):
        raise NotImplementedError

    def increase_nb_users_cached(self, nb_cached):
        raise NotImplementedError
    
class AsyncClient:
    '''
    async client
    '''
    async def add_user(self, user, transaction=None):
        raise NotImplementedError

    async def get_users(self, transaction=None):
        raise NotImplementedError

    async def increase_nb_users_cached(self, nb_cached, transaction=None):
        raise NotImplementedError

async def cache_users_async(client, cache):
    '''
    param client [Client/AsyncClient] client instance
    param cache [dict] result
    '''
    users = await client.get_users()
    
    nb_users_cached = 0
    for user in users:
        if user.id not in cache:
            nb_users_cached += 1
            cache[user.id] = user

    await client.increase_nb_users_cached(nb_users_cached)
    logging.debug("receive clients")
    return nb_users_cached

class TestUsingCoroutineMock(asynctest.TestCase):
    async def test_no_users_to_add(self):
        '''
        using asynctest.CoroutineMock for coroutine functions,
        if func not defined by 'async def'
        '''
        client = asynctest.Mock(Client())
        client.get_users = asynctest.CoroutineMock(return_value=[])
        client.increase_nb_users_cached = asynctest.CoroutineMock()
        cache = {}

        with asynctest.patch("logging.debug") as debug_mock:
            nb_added = await cache_users_async(client, cache)

        client.get_users.assert_awaited()
        self.assertEqual(nb_added, 0)
        self.assertEqual(len(cache), 0)

        client.increase_nb_users_cached.assert_awaited_once_with(0)

        debug_mock.assert_called()

    @asynctest.patch("logging.debug")
    async def test_no_users_to_add_2(self, debug_mock):
        '''
        if func is defined by 'async def', it's NOT MUST use
        asynctest.CoroutineMock(), asynctest will detect
        '''
        client = asynctest.Mock(AsyncClient())
        client.get_users.return_value = []
        cache = {}

        nb_added = await cache_users_async(client, cache)

        client.get_users.assert_awaited()
        self.assertEqual(nb_added, 0)
        self.assertEqual(len(cache), 0)

        client.increase_nb_users_cached.assert_awaited_once_with(0)
        
        debug_mock.assert_called()
