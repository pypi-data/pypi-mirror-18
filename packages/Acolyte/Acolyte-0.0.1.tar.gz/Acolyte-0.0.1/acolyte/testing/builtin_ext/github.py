import simplejson as json
from acolyte.testing import EasemobFlowTestCase, MockContext
from acolyte.builtin_ext.github import (
    GithubPushJob,
    TravisCIJob,
)
from acolyte.util.lang import get_from_nested_dict


class GithubPushJobTestCase(EasemobFlowTestCase):

    def setUp(self):
        self._ctx = MockContext(
            executor=None,
            config={},
            flow_instance_id=0,
            job_instance_id=0,
            job_action_id=0,
            current_step="github_push"
        )
        self._github_push_job = GithubPushJob()

    def testTrigger(self):
        with open("resource/testing/github_push_res.json") as f:
            hook_data = json.loads(f.read())
        self._github_push_job.on_trigger(self._ctx, hook_data)
        self.assertEqual(
            get_from_nested_dict(
                self._ctx.saved_data, 0, 0, 0, "pusher", "email"),
            "hongze.chi@gmail.com"
        )


class TravisCIJobTestCase(EasemobFlowTestCase):

    def setUp(self):
        self._ctx = MockContext(
            executor=None,
            config={
                "jar_saved_dir": "/tmp",
                "jar_download_base_url": "http://127.0.0.1/jars"
            },
            flow_instance_id=0,
            job_instance_id=0,
            job_action_id=0,
            current_step="travis"
        )
        self._travis_ci_job = TravisCIJob()

    def testTrigger(self):
        self._travis_ci_job.on_trigger(self._ctx)
        self.assertIsNotNone(
            get_from_nested_dict(self._ctx.saved_data, 0, 0, 0, "begin_time"))

    def testOnBuildFinish(self):

        with open("resource/testing/base64_jar", "r") as f:
            base64_code = f.read()

        # 构建正常
        self._travis_ci_job.on_build_finish(
            self._ctx,
            build_result=0,
            test_result={
            },
            findbug_result={
            },
            jar_file_name="testjar.jar",
            jar_base64=base64_code
        )

        self.assertIsNotNone(self._ctx["jar_download_url"])
        self.assertEqual(
            get_from_nested_dict(
                self._ctx.saved_data, 0, 0, 0, "build_result"), 0)
        self.assertIsNotNone(
            get_from_nested_dict(
                self._ctx.saved_data, 0, 0, 0, "jar_download_url"))
