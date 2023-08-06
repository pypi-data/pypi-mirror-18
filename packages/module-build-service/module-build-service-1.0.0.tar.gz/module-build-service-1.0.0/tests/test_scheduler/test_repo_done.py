# Copyright (c) 2016  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Ralph Bean <rbean@redhat.com>

import unittest
import mock

import module_build_service.messaging
import module_build_service.scheduler.handlers.repos
import module_build_service.models


class TestRepoDone(unittest.TestCase):

    def setUp(self):
        self.config = mock.Mock()
        self.config.rpms_default_repository = 'dist_git_url'
        self.config.koji_profile = 'staging'  # TODO - point at a fake test config


        self.session = mock.Mock()
        self.fn = module_build_service.scheduler.handlers.repos.done

    @mock.patch('module_build_service.models.ModuleBuild.from_repo_done_event')
    def test_no_match(self, from_repo_done_event):
        """ Test that when a repo msg hits us and we have no match,
        that we do nothing gracefully.
        """
        from_repo_done_event.return_value = None
        msg = module_build_service.messaging.KojiRepoChange(
            'no matches for this...', '2016-some-guid-build')
        self.fn(config=self.config, session=self.session, msg=msg)

    @mock.patch('module_build_service.builder.KojiModuleBuilder.buildroot_ready')
    @mock.patch('module_build_service.builder.KojiModuleBuilder.get_session')
    @mock.patch('module_build_service.builder.KojiModuleBuilder.build')
    @mock.patch('module_build_service.builder.KojiModuleBuilder.buildroot_connect')
    @mock.patch('module_build_service.models.ModuleBuild.from_repo_done_event')
    @mock.patch('module_build_service.utils.at_concurrent_component_threshold',
                return_value=False)
    def test_a_single_match(self, threshold, from_repo_done_event, connect, build_fn, config, ready):
        """ Test that when a repo msg hits us and we have a single match.
        """
        config.return_value = mock.Mock(), "development"
        unbuilt_component_build = mock.Mock()
        unbuilt_component_build.package = 'foo'
        unbuilt_component_build.scmurl = 'full_scm_url'
        unbuilt_component_build.state = None
        unbuilt_component_build.batch = 2
        built_component_build = mock.Mock()
        built_component_build.package = 'foo2'
        built_component_build.scmurl = 'full_scm_url'
        built_component_build.state = 1
        built_component_build.batch = 2
        module_build = mock.Mock()
        module_build.batch = 1
        module_build.component_builds = [unbuilt_component_build, built_component_build]
        module_build.current_batch.return_value = [built_component_build]
        build_fn.return_value = 1234, 1, "", None

        from_repo_done_event.return_value = module_build

        ready.return_value = True

        msg = module_build_service.messaging.KojiRepoChange(
            'no matches for this...', '2016-some-guid-build')
        self.fn(config=self.config, session=self.session, msg=msg)
        build_fn.assert_called_once_with(artifact_name='foo', source='full_scm_url')

    @mock.patch('module_build_service.builder.KojiModuleBuilder.buildroot_ready')
    @mock.patch('module_build_service.builder.KojiModuleBuilder.get_session')
    @mock.patch('module_build_service.builder.KojiModuleBuilder.build')
    @mock.patch('module_build_service.builder.KojiModuleBuilder.buildroot_connect')
    @mock.patch('module_build_service.models.ModuleBuild.from_repo_done_event')
    @mock.patch('module_build_service.utils.at_concurrent_component_threshold',
                return_value=False)
    def test_a_single_match_build_fail(self, threshold, from_repo_done_event, connect, build_fn, config, ready):
        """ Test that when a KojiModuleBuilder.build fails, the build is
        marked as failed with proper state_reason.
        """
        config.return_value = mock.Mock(), "development"
        unbuilt_component_build = mock.Mock()
        unbuilt_component_build.package = 'foo'
        unbuilt_component_build.scmurl = 'full_scm_url'
        unbuilt_component_build.state = None
        unbuilt_component_build.batch = 2
        built_component_build = mock.Mock()
        built_component_build.package = 'foo2'
        built_component_build.scmurl = 'full_scm_url'
        built_component_build.state = 1
        built_component_build.batch = 2
        module_build = mock.Mock()
        module_build.batch = 1
        module_build.component_builds = [unbuilt_component_build, built_component_build]
        module_build.current_batch.return_value = [built_component_build]
        build_fn.return_value = None, 4, "Failed to submit artifact foo to Koji", None

        from_repo_done_event.return_value = module_build

        ready.return_value = True

        msg = module_build_service.messaging.KojiRepoChange(
            'no matches for this...', '2016-some-guid-build')
        self.fn(config=self.config, session=self.session, msg=msg)
        build_fn.assert_called_once_with(artifact_name='foo', source='full_scm_url')
        self.assertEquals(unbuilt_component_build.state_reason, "Failed to submit artifact foo to Koji")
