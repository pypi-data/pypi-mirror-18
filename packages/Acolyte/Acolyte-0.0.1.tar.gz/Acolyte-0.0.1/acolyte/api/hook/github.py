import requests
import simplejson as json
from acolyte.api import BaseAPIHandler


TOKEN = "f05f5f2d8b5e19f7d2e1b4eb48d5cf08d3918256"


class GithubEventHandler(BaseAPIHandler):

    def post(self):
        hook_data = json.loads(self.request.body)

        if hook_data.get("ref") != "refs/heads/dev":
            return

        # 创建新的Flow Intstance
        rs = requests.post(
            "http://localhost:8888/v1/flow/template/eldermob_flow/start",
            json={"description": "eldermob服务更新", "start_flow_args": {}},
            headers={"token": TOKEN})
        print(rs.json())

        # 执行github push job
        rs = requests.post(
            (
                "http://localhost:8888/v1/flow/template/"
                "eldermob_flow/github_push/trigger"
            ),
            json={"action_args": {"hook_data": hook_data}},
            headers={"token": TOKEN}
        )
        print(rs.json())
