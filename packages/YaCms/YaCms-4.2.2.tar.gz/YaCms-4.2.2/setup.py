
import os
import sys
from setuptools import setup, find_packages
from shutil import rmtree
from yacms import __version__ as version


exclude = ["yacms/project_template/dev.db",
           "yacms/project_template/project_name/local_settings.py"]
if sys.argv == ["setup.py", "test"]:
    exclude = []
exclude = dict([(e, None) for e in exclude])

for e in exclude:
    if e.endswith(".py"):
        try:
            os.remove("%sc" % e)
        except:
            pass
    try:
        with open(e, "r") as f:
            exclude[e] = (f.read(), os.stat(e))
        os.remove(e)
    except:
        pass

if sys.argv[:2] == ["setup.py", "bdist_wheel"]:
    # Remove previous build dir when creating a wheel build,
    # since if files have been removed from the project,
    # they'll still be cached in the build dir and end up
    # as part of the build, which is really neat!
    try:
        rmtree("build")
    except:
        pass

try:
    setup(
        name="YaCms",
        version=version,
        author="Andrew Ho",
        author_email="hoangminh.it4u@gmail.com",
        description="An open source content management platform built using "
                    "the Django framework.",
        long_description=open("README.rst", 'rb').read().decode('utf-8'),
        license="BSD",
        url="https://github.com/minhhoit/yacms",
        download_url = 'https://github.com/minhhoit/yacms/tarball/1.0',
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            "django-contrib-comments",
            "django >= 1.8, < 1.11",
            "filebrowser_safe >= 0.4.6",
            "grappelli_safe >= 0.4.5",
            "tzlocal >= 1.0",
            "bleach >= 1.4",
            "beautifulsoup4 >= 4.1.3",
            "requests >= 2.1.0",
            "requests-oauthlib >= 0.4",
            "future >= 0.9.0",
            "pillow",
            "chardet",
        ],
        entry_points="""
            [console_scripts]
            yacms-project=yacms.bin.yacms_project:create_project
        """,
        test_suite="yacms.bin.runtests.main",
        tests_require=["pyflakes>=0.6.1", "pep8>=1.4.1"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ])
finally:
    for e in exclude:
        if exclude[e] is not None:
            data, stat = exclude[e]
            try:
                with open(e, "w") as f:
                    f.write(data)
                os.chown(e, stat.st_uid, stat.st_gid)
                os.chmod(e, stat.st_mode)
            except:
                pass
