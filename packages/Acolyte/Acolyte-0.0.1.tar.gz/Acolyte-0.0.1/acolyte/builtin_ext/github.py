import datetime
from acolyte.core.job import (
    AbstractJob,
    JobRef,
    action_args,
    ActionArg,
    Decision,
    DecisionOption,
    Jinja2DetailsPageUI,
)
from acolyte.util.time import common_fmt_dt
from acolyte.util.validate import Field, StrField
from acolyte.core.flow import FlowMeta
from acolyte.util.mail import send_mail
from acolyte.ui import Button
from jinja2 import Environment, PackageLoader


jinja2_env = Environment(
    loader=PackageLoader('acolyte.builtin_ext', 'github_ui'))
email_template = jinja2_env.get_template("mail_template.html")


def _get_decision_url(context, decision_name):
    decision_url = (
        "http://{host}/job/instance/{instance_id}"
        "/decision/{decision_name}"
    ).format(
        host=context.config["host"],
        instance_id=context.job_instance_id,
        decision_name=decision_name
    )
    return decision_url


def _get_flow_instance_url(context):
    flow_instance_url = (
        "http://{host}/flow/instance/{instance_id}"
    ).format(
        host=context.config["host"],
        instance_id=context.flow_instance_id
    )
    return flow_instance_url


class GithubPushJob(AbstractJob):

    """接受github push事件
    """

    def __init__(self):
        super().__init__(
            name="github_push",
            description=(
                "This job could handle github push event."
            )
        )

    @action_args(
        ActionArg(
            Field("hook_data", type_=dict, required=True),
            mark=ActionArg.MARK_AUTO, comment="github hook 接收的数据"),
    )
    def on_trigger(self, context, hook_data):
        """
        :param hook_data: Github hook返回的数据
        """

        # 要保存的数据结构

        """
        {

            "ref": "refs/heads/master",

            "commits": [
                {
                    "id": ...,
                    "message": ...,
                    "time": ...,
                    "committer": {
                        "name": "chihz",
                        "email": "hongze.chi@gmail.com",
                    },
                    "added": [

                    ],
                    "removed": [

                    ],
                    "modified": [
                        "README.md"
                    ]
                }
            ],

            "pusher": {
                "name": "chihongze",
                "email": "hongze.chi@gmail.com"
            }
        }
        """

        saved_data = {
            "ref": hook_data["ref"],

            "commits": [{
                "id": commit["id"],
                "message": commit["message"],
                "time": commit["timestamp"],
                "commiter": commit["committer"],
                "added": commit["added"],
                "removed": commit["removed"],
                "modified": commit["modified"]
            } for commit in hook_data["commits"]],

            "pusher": hook_data["pusher"]
        }

        context.save(saved_data)
        context.finish()


class TravisCIJob(AbstractJob):

    """处理Travis CI的构建
    """

    def __init__(self):
        super().__init__(
            name="travis",
            description="收集travis ci的执行结果",
            ui=Jinja2DetailsPageUI(jinja2_env, "travis_build.html")
        )

        # 只有当travis构建成功并且代码review也成功的时候该Job才会完成
        self._check_code_barrier = ["build_finish", "code_review"]

    def on_trigger(self, context):
        """触发时记录只记录构建的开始时间
        """
        context.save({"begin_time": common_fmt_dt(datetime.datetime.now())})

    @action_args(
        ActionArg(
            Field("build_result", type_=int, required=True),
            mark=ActionArg.MARK_AUTO,
            comment="Travis CI构建结果 0 - 成功， 1 - 失败"
        ),
        ActionArg(
            Field("test_result", type_=dict, required=True),
            mark=ActionArg.MARK_AUTO, comment="测试结果"
        ),
        ActionArg(
            Field("findbug_result", type_=dict, required=True),
            mark=ActionArg.MARK_AUTO, comment="findbugs检查结果"
        ),
        ActionArg(
            Field("jar_file_name", type_=str, required=False),
            mark=ActionArg.MARK_AUTO, comment="Jar包文件名称"
        ),
        ActionArg(
            Field("jar_base64", type_=str, required=False),
            mark=ActionArg.MARK_AUTO, comment="Jar包文件的BASE64编码"
        )
    )
    def on_build_finish(
            self, context, build_result, test_result, findbug_result,
            jar_file_name, jar_base64):
        """当TravisCI构建完成后执行此动作
           :param build_result: 构建结果，即TRAVIS_TEST_RESULT
           :param test_result: 测试结果 [
                {
                    "testsuite": "chihz.bot.elder.ElderServiceTestCase",
                    "skipped": 0,
                    "failures": 1,
                    "errors": 0,
                    "testcases": [
                        {
                            "name":
                                "chihz.bot.elder.ElderServiceTestCase.testAnswerQuestion",
                            "status": "failure",
                            "failure_type": "org.junit.ComparisonFailure",
                            "traceback": ...
                        },
                    ]
                },
                ...
           ]
           :param findbug_result: [
                {
                    "bug_type": "DM_BOXED_PRIMITIVE_FOR_PARSING",
                    "bug_category": "performance",
                    "bug_description":
                        "Comparison of String parameter using == or != in",
                    "details": "xxxx"
                }
           ]
           :param jar_file_name: jar包文件名
           :param jar_base64: jar包文件的base64编码
        """

        # 处理构建成功
        if build_result == 0:

            jar_download_url = "http://{base_url}/{jar_file_name}".format(
                base_url=context.config["jar_download_base_url"],
                jar_file_name=jar_file_name
            )

            context.save({
                "build_result": build_result,
                "test_result": test_result,
                "findbug_result": findbug_result,
                "jar_download_url": jar_download_url
            })

            context["jar_download_url"] = jar_download_url

            context.finish(waiting_for=self._check_code_barrier)

        # 处理构建失败
        else:

            context.save({
                "build_result": build_result,
                "test_result": test_result,
                "findbug_result": findbug_result,
            })

            context.failure()  # 终止整个流程

    @action_args(
        ActionArg(
            Field("code_review_result",
                  required=False, type_=bool, value_of=bool, default=False),
            mark=ActionArg.MARK_AUTO,
            comment="代码review结果"
        )
    )
    def on_code_review(self, context, code_review_result):
        if code_review_result:
            context.finish(waiting_for=self._check_code_barrier)
        else:
            context.failure()  # 不通过会终止整个工作流


class SandboxJob(AbstractJob):

    """部署到测试沙箱
    """

    def __init__(self):
        super().__init__(
            name="sandbox",
            description="该Job可以将Jar包部署到Sandbox",
            decisions=[
                Decision(
                    "do_deploy", "部署到沙箱", "部署当前版本到沙箱",
                    DecisionOption("deploy", "执行自动部署脚本")
                ),
                Decision(
                    "deploy_sandbox", "反馈部署结果", "当前是否可以部署到沙箱？",
                    DecisionOption("agree", "可以部署"),
                    DecisionOption("disagree", "无法部署")
                ),
            ],
            auto_trigger=True
        )

    def on_trigger(self, context):
        """被触发之后会先给运维发个邮件
        """

        sandbox_deployer_email = context.config["sandbox_deployer_email"]

        flow_details_url = _get_flow_instance_url(context)
        decision_url = _get_decision_url(context, "deploy_sandbox")

        send_mail(
            receiver=sandbox_deployer_email,
            subject="有新的版本需要您部署到沙箱",
            content=email_template.render(
                prompt="有新的版本需要您部署到沙箱，请您执行部署之后反馈部署结果，谢谢 : )",
                buttons=(
                    Button("查看流程", flow_details_url),
                    Button("反馈部署结果", decision_url)
                )
            )
        )

    def on_deploy(self, context):
        ...

    @action_args(
        ActionArg(
            StrField("test_service_url", required=True),
            mark=ActionArg.MARK_AUTO, comment="部署完毕后的测试地址"
        )
    )
    def on_agree(self, context, test_service_url):
        """当同意部署的时候会触发该事件，调用运维的接口自动部署到沙箱环境
        """
        context.save({"test_service_url": test_service_url})
        context["test_service_url"] = test_service_url
        context.finish()

    @action_args(
        ActionArg(StrField("reason", required=True),
                  mark=ActionArg.MARK_AUTO, comment="不同意部署的原因")
    )
    def on_disagree(self, context, reason):
        """不同意部署，会产生一个原因
        """
        context.save({"reason": reason})
        context.failure()


class IntegrationTestJob(AbstractJob):

    """集成测试
    """

    def __init__(self):
        super().__init__(
            name="integration_test",
            description=(
                "job for integration test"
            ),
            decisions=(
                Decision(
                    "do_test", "执行集成测试", "运行集成测试用例",
                    DecisionOption("test", "执行测试"),),
                Decision(
                    "test_result", "反馈测试结果", "集成测试结果反馈",
                    DecisionOption("pass", "测试通过"),
                    DecisionOption("failure", "有点问题")
                ),
            ),
            auto_trigger=True
        )

    def on_trigger(self, context):
        qa_email = context.config["qa_email"]

        decision_url = _get_decision_url(context, "test_result")
        flow_instance_url = _get_flow_instance_url(context)

        send_mail(
            receiver=qa_email,
            subject="沙箱中有新的版本需要测试了",
            content=email_template.render(
                prompt="沙箱中有新的版本需要测试，请您测试之后反馈结果，谢谢: )",
                buttons=(
                    Button("查看流程", flow_instance_url),
                    Button("反馈测试结果", decision_url)
                )
            )
        )

    def on_test(self, context):
        pass

    def on_pass(self, context):
        """测试通过
        """
        context.save({
            "test_result": "success"
        })
        context.finish()

    @action_args(
        ActionArg(
            StrField("reason", required=True),
            mark=ActionArg.MARK_AUTO, comment="测试不通过的原因"
        )
    )
    def on_failure(self, context, reason):
        """测试失败
        """
        context.save({
            "test_result": "failure",
            "reason": reason
        })
        context.failure()


class MergeToMasterJob(AbstractJob):

    def __init__(self):
        super().__init__(
            name="merge_to_master",
            description=(
                "merge dev branch to master"
            ),
            auto_trigger=True
        )

    def on_trigger(self, context):
        # TODO Call github api
        context.finish()


class DeployJob(AbstractJob):

    def __init__(self):
        super().__init__(
            name="deploy",
            description=(
                "job for deploying to online server"
            ),
            auto_trigger=True,
            decisions=[
                Decision(
                    "do_deploy", "部署到线上", "部署到线上",
                    DecisionOption("deploy", "部署到线上"),
                ),
                Decision(
                    "deploy_result", "反馈部署结果", "部署结果反馈",
                    DecisionOption("success", "部署成功"),
                    DecisionOption("failure", "部署失败")
                )
            ]
        )

    def on_trigger(self, context):
        deployer_email = context.config["deployer_email"]
        flow_instance_url = _get_flow_instance_url(context)
        send_mail(
            receiver=deployer_email,
            subject="有新工程需要部署",
            content=email_template.render(
                prompt="有新的工程需要您部署，部署完毕后请反馈部署结果，谢谢: )",
                buttons=(
                    Button("查看流程", flow_instance_url),
                )
            )
        )

    def on_deploy(self, context):
        ...

    def on_success(self, context):
        context.finish()

    def on_failure(self, context):
        context.failure()


class CommonGithubFlowMeta(FlowMeta):

    def __init__(self):
        super().__init__(
            name="common_github_flow",
            description="常规的个人github项目流程",
            jobs=(

                # 接受github push
                JobRef("github_push"),

                # 处理TravisCI的构建结果
                JobRef("travis"),

                # 部署到沙箱
                JobRef("sandbox"),

                # 进行集成测试
                JobRef("integration_test"),

                # merge到master分支
                JobRef("merge_to_master"),

                # 部署到线上
                JobRef("deploy")
            )
        )

    def on_start(self, context):
        ...

    def on_failure(self, context):
        ...

    def on_finish(self, context):
        ...

    def on_discard(self, context):
        ...
