import sys
import requests
from acolyte.testing.mock import get_token


TOKEN = get_token("chihz@easemob.com", "123456")


def main():
    mock_action = sys.argv[1]

    if mock_action == "trigger":
        mock_trigger()
    elif mock_action == "build_finish":
        mock_build_finish(sys.argv[2])
    elif mock_action == "code_review":
        mock_code_review(sys.argv[2])


def mock_trigger():
    rs = requests.post(
        (
            "http://localhost:8888/v1/flow/template/"
            "eldermob_flow/travis/trigger"
        ),
        json={"action_args": {}},
        headers={"token": TOKEN}
    )
    print(rs.json())


def mock_build_finish(build_result):
    if build_result == "success":
        action_args = {
            "build_result": 0,
            "test_result": {},
            "findbug_result": {},
            "jar_file_name": "test_service_20160927_release.jar",
            "jar_base64": "aGVoZQo="
        }
    else:
        action_args = {
            "build_result": 1,
            "test_result": {},
            "findbug_result": {},
            "jar_file_name": "",
            "jar_base64": ""
        }

    rs = requests.post(
        (
            "http://localhost:8888/v1/flow/template/"
            "eldermob_flow/travis/build_finish"
        ),
        json={"action_args": action_args},
        headers={"token": TOKEN}
    )

    print(rs.json())


def mock_code_review(code_review_result):
    if code_review_result == "success":
        action_args = {
            "code_review_result": "1"
        }
    else:
        action_args = {}

    rs = requests.post(
        (
            "http://localhost:8888/v1/flow/template/"
            "eldermob_flow/travis/code_review"
        ),
        json={
            "action_args": action_args
        },
        headers={"token": TOKEN}
    )

    print(rs.json())


if __name__ == "__main__":
    main()
