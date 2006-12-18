#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2006 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

import os, sys, traceback

for toplevel in [".", "..", "../..", "../../..", "../../../.."]:
    toplevel = os.path.normpath(toplevel)
    if os.path.exists(os.path.join(toplevel, "python", "Ice.py")):
        break
else:
    raise "can't find toplevel directory!"

sys.path.insert(0, os.path.join(toplevel, "python"))
sys.path.insert(0, os.path.join(toplevel, "lib"))

import Ice
Ice.loadSlice('Test.ice')
import Test

def test(b):
    if not b:
        raise RuntimeError('test assertion failed')

class CustomI(Test.Custom):
    def __init__(self, adapter):
        self._adapter = adapter

    def opByteString1(self, b1, current=None):
	test(isinstance(b1, str))
	return (b1, b1)

    def opByteString2(self, b1, current=None):
	test(isinstance(b1, list))
	return (b1, b1)

    def opByteList1(self, b1, current=None):
	test(isinstance(b1, list))
	return (b1, b1)

    def opByteList2(self, b1, current=None):
	test(isinstance(b1, tuple))
	return (b1, b1)

    def opStringList1(self, s1, current=None):
	test(isinstance(s1, list))
	return (s1, s1)

    def opStringList2(self, s1, current=None):
	test(isinstance(s1, tuple))
	return (s1, s1)

    def opStringTuple1(self, s1, current=None):
	test(isinstance(s1, tuple))
	return (s1, s1)

    def opStringTuple2(self, s1, current=None):
	test(isinstance(s1, list))
	return (s1, s1)

    def sendS(self, val, current=None):
	test(isinstance(val.b1, str))
	test(isinstance(val.b2, list))
	test(isinstance(val.b3, str))
	test(isinstance(val.b4, list))
	test(isinstance(val.s1, list))
	test(isinstance(val.s2, tuple))
	test(isinstance(val.s3, tuple))
	test(isinstance(val.s4, list))

    def sendC(self, val, current=None):
	test(isinstance(val.b1, str))
	test(isinstance(val.b2, list))
	test(isinstance(val.b3, str))
	test(isinstance(val.b4, list))
	test(isinstance(val.s1, list))
	test(isinstance(val.s2, tuple))
	test(isinstance(val.s3, tuple))
	test(isinstance(val.s4, list))

    def shutdown(self, current=None):
        self._adapter.getCommunicator().shutdown()

def run(args, communicator):
    communicator.getProperties().setProperty("Ice.OA.TestAdapter.Endpoints", "default -p 12010 -t 10000")
    adapter = communicator.createObjectAdapter("TestAdapter")
    object = CustomI(adapter)
    adapter.add(object, communicator.stringToIdentity("test"))
    adapter.activate()
    communicator.waitForShutdown()
    return True

try:
    communicator = Ice.initialize(sys.argv)
    status = run(sys.argv, communicator)
except:
    traceback.print_exc()
    status = False

if communicator:
    try:
        communicator.destroy()
    except:
        traceback.print_exc()
        status = False

sys.exit(not status)
