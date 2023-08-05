"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals

from dockerfile_parse import DockerfileParser
from atomic_reactor.inner import DockerBuildWorkflow
from atomic_reactor.plugin import PreBuildPluginsRunner
from atomic_reactor.plugins.pre_return_dockerfile import CpDockerfilePlugin
from atomic_reactor.util import ImageName
from tests.constants import MOCK_SOURCE
from tests.fixtures import docker_tasker


class Y(object):
    pass

class X(object):
    image_id = "xxx"
    source = Y()
    source.dockerfile_path = None
    source.path = None
    base_image = ImageName(repo="qwe", tag="asd")

def test_returndockerfile_plugin(tmpdir):
    df_content = """
FROM fedora
RUN yum install -y python-django
CMD blabla"""
    df = DockerfileParser(str(tmpdir))
    df.content = df_content

    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image')
    workflow.builder = X
    workflow.builder.df_path = df.dockerfile_path
    workflow.builder.df_dir = str(tmpdir)

    runner = PreBuildPluginsRunner(
        docker_tasker,
        workflow,
        [{
            'name': CpDockerfilePlugin.key
        }]
    )
    runner.run()
    assert CpDockerfilePlugin.key is not None

    assert workflow.prebuild_results.get(CpDockerfilePlugin.key, "") == df_content
