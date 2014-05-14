import inspect
import os

from nose.case import FunctionTestCase
from nose.plugins import Plugin
from nose.suite import ContextSuite, ContextSuiteFactory

class MultiThreadFunctionTestCase(FunctionTestCase):

    def runTest(self):
        super(MultiThreadFunctionTestCase, self).runTest()


class MultiThreadContextSuite(ContextSuite):

    def run(self, result):
        """Run tests in suite inside of suite fixtures.
        """
        # proxy the result for myself
        #log.debug("suite %s (%s) run called, tests: %s", id(self), self, self._tests)
        #import pdb
        #pdb.set_trace()
        if self.resultProxy:
            result, orig = self.resultProxy(result, self), result
        else:
            result, orig = result, result
        try:
            self.setUp()
        except KeyboardInterrupt:
            raise
        except:
            self.error_context = 'setup'
            result.addError(self, self._exc_info())
            return
        try:
            for test in self._tests:
                if result.shouldStop:
                    log.debug("stopping")
                    break
                # each nose.case.Test will create its own result proxy
                # so the cases need the original result, to avoid proxy
                # chains
                test(orig)
        finally:
            self.has_run = True
            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                self.error_context = 'teardown'
                result.addError(self, self._exc_info())


class MultiThread(Plugin):
    name = "multithread"

    def options(self, parser, env=os.environ):
        super(MultiThread, self).options(parser, env=env)

    def configure(self, options, conf):
        super(MultiThread, self).configure(options, conf)
        if not self.enabled:
            return
        ContextSuiteFactory.suiteClass = MultiThreadContextSuite

    def makeTest(self, obj, parent):
        if inspect.isfunction(obj):
            yield MultiThreadFunctionTestCase(obj)
