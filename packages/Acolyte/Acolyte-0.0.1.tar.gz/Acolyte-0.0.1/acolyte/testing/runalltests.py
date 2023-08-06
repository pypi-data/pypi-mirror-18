import nose
import pkgutil
import acolyte.testing

excludes = {
    "acolyte.testing.util.mail",  # 邮件模块无需测试
    "acolyte.testing.builtin_ext.github",
    "acolyte.testing.builtin_ext.mock_push",
    "acolyte.testing.builtin_ext.mock_travis",
    "acolyte.testing.core.notify_logic",
}


def main():
    argv = [
        "",
        (
            "--with-xunit"
        ),
    ]
    for importer, modname, ispkg in pkgutil.walk_packages(
            path=acolyte.testing.__path__,
            prefix="acolyte.testing."):
        if ispkg:
            continue
        if modname in excludes:
            continue
        argv.append(modname)
    nose.run(argv=argv)


if __name__ == "__main__":
    main()
