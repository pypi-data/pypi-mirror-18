import requests
import simplejson as json
from acolyte.testing.mock import get_token


TOKEN = get_token("chihz@easemob.com", "123456")


def main():
    with open("resource/testing/github_push_res.json", "r") as f:
        hook_data = json.loads(f.read())
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


if __name__ == "__main__":
    main()
