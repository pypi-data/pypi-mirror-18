import setuptools
from acolyte import VERSION

install_requires = [
    "Jinja2 >= 2.8",
    "PyGithub >= 1.29",
    "PyMySQL >= 0.7.9",
    "fixtures >= 3.0.0",
    "nose >= 1.3.7",
    "requests >= 2.11.1",
    "simplejson >= 3.8.2",
    "tornado >= 4.4.2",
    "tornado_jinja2 >= 0.2.4",
    "retrying >= 1.3.3",
    "docker-py >= 1.10.4",
    "python-jenkins >= 0.4.13",
    "xmltodict >= 0.10.2",
]

setuptools.setup(
    name="Acolyte",
    version=VERSION,
    author="ChiHongze",
    author_email="chihz@easemob.com",
    url='https://github.com/easemob/acolyte',
    description="An interactive workflow framework, you can use it to build "
    "CI, CD system",
    license="MIT",
    packages=setuptools.find_packages("."),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [

        ],
        "acolyte.job": [
            # mooncake jobs
            "programmer = acolyte.builtin_ext.mooncake:ProgrammerJob",
            "hr = acolyte.builtin_ext.mooncake:HRJob",
            "boss = acolyte.builtin_ext.mooncake:BossJob",
        ],
        "acolyte.flow_meta": [
            # moon cake flow
            "mooncake_flow = acolyte.builtin_ext.mooncake:MooncakeFlowMeta"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
)
