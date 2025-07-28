from pybuilder.core import use_plugin, init, task, depends

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.install_dependencies")

name = "flask_mysql_crud"
version = "1.0.0"
default_task = ["default"]

@init
def set_properties(project):
    project.build_depends_on("Flask")
    project.build_depends_on("mysql-connector-python")
    project.set_property("dir_source_main_python", "src/main/python")
    project.set_property("dir_source_unittest_python", "src/unittest/python")
    project.set_property("unittest_module_glob", "test_*.py")
    project.set_property("coverage_break_build", False)
    project.set_property("coverage_threshold_warn", 80)
    project.set_property("coverage_threshold_fail", 50)

@task
def run_flask_app(project, logger):
    import subprocess
    logger.info("Starting Flask app for development...")
    subprocess.call(["python", "src/main/python/app.py"])

@task
@depends("run_unit_tests", "coverage")
def run_tests_and_coverage():
    pass

@task
@depends("run_tests_and_coverage")
def default():
    pass
