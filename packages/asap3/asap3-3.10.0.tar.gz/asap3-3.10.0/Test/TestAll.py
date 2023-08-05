"""
A simple test script.

Runs and times all scripts named ``*.py``.  The tests that execute
the fastest will be run first.
"""
from __future__ import print_function

#PBS -m ae
#PBS -q medium

## Tell asap-qsub that there is per default no threading.
#ASAP N

import glob
import time
import pickle
import sys
import gc
try:
    import StringIO
except ImportError:
    # Python 3?
    import io as StringIO
from optparse import OptionParser
import asap3
import os
from ase.parallel import paropen

from asap3.mpi import world
master = world.rank == 0


if master:
    print("")
    print("*** Running ASAP Test Suite ***")
    print("")
    asap3.print_version(1)
    
brokentests = [
               'PrintMemory.py',  # Not really broken, but prints to stderr
               'EMTleak.py',      # Prints to stderr
               'Exception.py',    # Does not work with testsuite.
               # REALLY BROKEN TESTS
               'BrennerNanotube.py',  # Leaks memory (bug in numpy)
               'BrennerStress.py',    # Must be completed.
               'OpenKIM_AllModels.py',  # Tests the models, not Asap.  Some fail.
               'RDF2.py',
               'Hydrocarbons.py',
               'FieldPlotter.py',    # Fails on machines without gs or netpbm
               'bundleTrajPreserveZ.py',  # Fails on buildbot due to old ASE.
               ]

slowtests = ['HooverNPT.py', 'HooverNPTtraj.py', 'Langevin.py',
             'LongLangevin.py', 'TinyLangevin.py',
             'parallelLennardJones.py',
             'parallelLangevin.py', 'parallelLongVerlet.py']

stdout = sys.stdout
stderr = sys.stderr
if not master:
    stdout = sys.stdout = open(("TestAll-proc%d.out" % (world.rank)), "w")

parser = OptionParser(usage='%prog [options] [tests]',
                      version='%prog 0.1')

parser.add_option('-x', '--exclude',
                  type='string', default=None,
                  help='Exclude tests (comma separated list of tests).',
                  metavar='test1.py,test2.py,...')

parser.add_option('-f', '--run-failed-tests-only',
                  action='store_true',
                  help='Run failed tests only.')

parser.add_option('-p', '--parallel',
                  action='store_true',
                  help='Run parallel tests only.')

parser.add_option('-s', '--slow',
                  action='store_true',
                  help='Also run slow tests.')

parser.add_option('-t', '--threads',
                  action='store_true',
                  help='Run with threading enabled.')

parser.add_option('-T', '--forcethreads',
                  action='store_true',
                  help='Run with threading enabled (4 threads forced).')

parser.add_option('-v', '--view-output',
                  action='store_true',
                  help="View output of all tests instead of redirecting them.")

options, tests = parser.parse_args()

# Clear the arguments, so we do not trouble the tests.
del sys.argv[1:]

if options.parallel:
    path = 'parallel/'
    print("Running in parallel on %d CPUs." % (world.size,))
else:
    path = ''

if options.threads:
    asap3.AsapThreads()
    
if options.forcethreads:
    asap3.AsapThreads(4, force=True)
    
if len(tests) == 0:
    tests = glob.glob(path + '*.py')

    exclude = ['__init__.py', 'TestAll.py'] + brokentests
    if options.exclude is not None:
        exclude += options.exclude.split(',')

    if not options.slow:
        exclude += slowtests
        if master:
            print("")
            print("Skipping slow tests (use --slow to include them):")
            for x in slowtests:
                print("   ", x)
            print("")

    for test in exclude:
        if path + test in tests:
            tests.remove(path + test)
    
gc.set_debug(gc.DEBUG_SAVEALL)

# Read old timings if they are present:
try:
    timings = pickle.loads(open('timings.pickle', "rb").read())
except IOError:
    timings = {}

# Make a list of tests to do, and sort it with the fastest/new
# tests first:
tests = [(timings.get(test, 0.0), test) for test in tests]
tests.sort()

if options.run_failed_tests_only:
    tests = [(t, test) for t, test in tests if t == 0.0]

L = max([len(test) for told, test in tests])
print('-----------------------------------------------------------------')
print(' test', ' ' * (L - 4), 'result      time (old)')
print('-----------------------------------------------------------------')

leaktest = True
garbage = []
failed = []
# Do tests:
for told, test in tests:
    
    if not options.view_output:
        sys.stdout = StringIO.StringIO()
        sys.stderr = StringIO.StringIO()

    print('%-*s' % (L + 2, test), end=' ', file=stdout)
    stdout.flush()

    ok = False
    
    module = test[:-3]
    if options.parallel:
        module = module.replace('/', '.')
        
    t = time.time()
    try:
        xxxx = __name__
        __name__ = "__main__"
        module = __import__(module, globals(), locals(), [])
        del module
        __name_ = xxxx
    except KeyboardInterrupt:
        failed.append(test)
        print('STOPPED!', file=stdout)
        print(('Hit [enter] to continue with next test, ' +
                                  '[ctrl-C] to stop.'), file=stdout)
        try:
            raw_input()
        except KeyboardInterrupt:
            break
        continue
    except AssertionError as msg:
        print('FAILED!', file=stdout)
        print(msg, file=stdout)
    except:
        print('CRASHED!', file=stdout)
        type, value = sys.exc_info()[:2]
        print(str(type) + ":", value, file=stdout)
    else:
        ok = True
        
    t = time.time() - t

    gc.collect()
    n = len(gc.garbage)
    if n > 0 and leaktest:
        print(' LEAK!', file=stdout)
        print(('Uncollectable garbage (%d object%s)' %
                                  (n, 's'[:n > 1])), file=stdout)
        print("Further leak testing not possible", file=stdout)
        print(file=stdout)
        print("The first 10 leaked objects are:", file=stdout)
        for o in gc.garbage[:10]:
            print(repr(o), type(o), type(o).__module__, file=stdout)
            del o
        leaktest = False
        ok = False
    if ok:
        print('  OK     %7.3f (%.3f)' % (t, told), file=stdout)
    else:
        failed.append(test)
        if not options.view_output:
            out = sys.stdout.getvalue()
            if len(out) > 0 and master:
                open(test + '.output', 'w').write(out)
            err = sys.stderr.getvalue()
            if len(err) > 0 and master:
                open(test + '.error', 'w').write(err)
        t = 0
    timings[test] = t
        
if not options.view_output:
    sys.stdout = stdout
    sys.stderr = stderr

print('-----------------------------------------------------------------')

if len(tests) > 1:
    print()
    if len(failed) == 0:
        print('All tests passed!')
    elif len(failed) == 1:
        print('One test out of %d failed: %s' % (len(tests), failed[0]))
    else:
        print('%d tests out of %d failed:'% (len(failed), len(tests)))
        for test in failed:
            print(' ', test)
    print()

# Save new timings:
open('timings.pickle', 'wb').write(pickle.dumps(timings, protocol=2))

# Report the error to build bot.
failedname = "TestAll-failed.txt"
if len(failed):
    failedfile = paropen(failedname, "w")
    failedfile.write(str(len(failed))+'\n')
    failedfile.close()
else:
    if os.path.exists(failedname):
        os.remove(failedname)
