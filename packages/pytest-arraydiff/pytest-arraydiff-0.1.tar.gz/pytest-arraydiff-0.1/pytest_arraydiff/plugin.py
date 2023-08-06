# Copyright (c) 2016, Thomas P. Robitaille
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# This package was derived from pytest-mpl, which is released under a BSD
# license and can be found here:
#
#   https://github.com/astrofrog/pytest-mpl


from functools import wraps

import os
import sys
import shutil
import tempfile
import warnings

import pytest
import numpy as np

if sys.version_info[0] == 2:
    from urllib import urlopen
else:
    from urllib.request import urlopen


class FITSDiff(object):

    extension = 'fits'

    @staticmethod
    def read(filename):
        from astropy.io import fits
        return fits.getdata(filename)

    @staticmethod
    def write(filename, array, **kwargs):
        from astropy.io import fits
        return fits.writeto(filename, array, **kwargs)


class TextDiff(object):

    extension = 'txt'

    @staticmethod
    def read(filename):
        return np.loadtxt(filename)

    @staticmethod
    def write(filename, array, **kwargs):
        if 'fmt' not in kwargs:
            kwargs['fmt'] = '%g'
        return np.savetxt(filename, array, **kwargs)


FORMATS = {}
FORMATS['fits'] = FITSDiff
FORMATS['text'] = TextDiff


def _download_file(url):
    u = urlopen(url)
    result_dir = tempfile.mkdtemp()
    filename = os.path.join(result_dir, 'downloaded')
    with open(filename, 'wb') as tmpfile:
        tmpfile.write(u.read())
    return filename


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--arraydiff', action='store_true',
                    help="Enable comparison of arrays to reference arrays stored in files")
    group.addoption('--arraydiff-generate-path',
                    help="directory to generate reference files in, relative to location where py.test is run", action='store')
    group.addoption('--arraydiff-reference-path',
                    help="directory containing reference files, relative to location where py.test is run", action='store')
    group.addoption('--arraydiff-default-format',
                    help="Default format for the reference arrays (can be 'fits' or 'text' currently)")


def pytest_configure(config):

    if config.getoption("--arraydiff") or config.getoption("--arraydiff-generate-path") is not None:

        reference_dir = config.getoption("--arraydiff-reference-path")
        generate_dir = config.getoption("--arraydiff-generate-path")

        if reference_dir is not None and generate_dir is not None:
            warnings.warn("Ignoring --arraydiff-reference-path since --arraydiff-generate-path is set")

        if reference_dir is not None:
            reference_dir = os.path.abspath(reference_dir)
        if generate_dir is not None:
            reference_dir = os.path.abspath(generate_dir)

        default_format = config.getoption("--arraydiff-default-format") or 'text'

        config.pluginmanager.register(ArrayComparison(config,
                                                      reference_dir=reference_dir,
                                                      generate_dir=generate_dir,
                                                      default_format=default_format))


class ArrayComparison(object):

    def __init__(self, config, reference_dir=None, generate_dir=None, default_format='text'):
        self.config = config
        self.reference_dir = reference_dir
        self.generate_dir = generate_dir
        self.default_format = default_format

    def pytest_runtest_setup(self, item):

        compare = item.keywords.get('array_compare')

        if compare is None:
            return

        file_format = compare.kwargs.get('file_format', self.default_format)

        if file_format not in FORMATS:
            raise ValueError("Unknown format: {0}".format(file_format))

        if 'extension' in compare.kwargs:
            extension = compare.kwargs['extension']
        else:
            extension = FORMATS[file_format].extension

        atol = compare.kwargs.get('atol', 0.)
        rtol = compare.kwargs.get('rtol', 1e-7)

        single_reference = compare.kwargs.get('single_reference', False)

        write_kwargs = compare.kwargs.get('write_kwargs', {})

        original = item.function

        @wraps(item.function)
        def item_function_wrapper(*args, **kwargs):

            reference_dir = compare.kwargs.get('reference_dir', None)
            if reference_dir is None:
                if self.reference_dir is None:
                    reference_dir = os.path.join(os.path.dirname(item.fspath.strpath), 'reference')
                else:
                    reference_dir = self.reference_dir
            else:
                if not reference_dir.startswith(('http://', 'https://')):
                    reference_dir = os.path.join(os.path.dirname(item.fspath.strpath), reference_dir)

            baseline_remote = reference_dir.startswith('http')

            # Run test and get figure object
            import inspect
            if inspect.ismethod(original):  # method
                array = original(*args[1:], **kwargs)
            else:  # function
                array = original(*args, **kwargs)

            # Find test name to use as plot name
            filename = compare.kwargs.get('filename', None)
            if filename is None:
                if single_reference:
                    filename = original.__name__ + '.' + extension
                else:
                    filename = item.name + '.' + extension
                    filename = filename.replace('[', '_').replace(']', '_')
                    filename = filename.replace('_.' + extension, '.' + extension)

            # What we do now depends on whether we are generating the reference
            # files or simply running the test.
            if self.generate_dir is None:

                # Save the figure
                result_dir = tempfile.mkdtemp()
                test_image = os.path.abspath(os.path.join(result_dir, filename))

                FORMATS[file_format].write(test_image, array, **write_kwargs)

                # Find path to baseline image
                if baseline_remote:
                    baseline_file_ref = _download_file(reference_dir + filename)
                else:
                    baseline_file_ref = os.path.abspath(os.path.join(os.path.dirname(item.fspath.strpath), reference_dir, filename))

                if not os.path.exists(baseline_file_ref):
                    raise Exception("""File not found for comparison test
                                    Generated file:
                                    \t{test}
                                    This is expected for new tests.""".format(
                        test=test_image))

                # distutils may put the baseline images in non-accessible places,
                # copy to our tmpdir to be sure to keep them in case of failure
                baseline_file = os.path.abspath(os.path.join(result_dir, 'reference-' + filename))
                shutil.copyfile(baseline_file_ref, baseline_file)

                array_ref = FORMATS[file_format].read(baseline_file)

                try:
                    np.testing.assert_allclose(array_ref, array, atol=atol, rtol=rtol)
                except AssertionError as exc:
                    message = "\n\na: {0}".format(test_image) + '\n'
                    message += "b: {0}".format(baseline_file) + '\n'
                    message += exc.args[0]
                    raise AssertionError(message)

                shutil.rmtree(result_dir)

            else:

                if not os.path.exists(self.generate_dir):
                    os.makedirs(self.generate_dir)

                FORMATS[file_format].write(os.path.abspath(os.path.join(self.generate_dir, filename)), array, **write_kwargs)

                pytest.skip("Skipping test, since generating data")

        if item.cls is not None:
            setattr(item.cls, item.function.__name__, item_function_wrapper)
        else:
            item.obj = item_function_wrapper
