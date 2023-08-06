import os

from utils.runCommand import run_cmd

CHECK_SPARK_HOME = """
if [ -z "$SPARK_HOME" ]; then
   echo "Error: SPARK_HOME is not set, can't run tests."
   exit 1
fi
"""
os.system(CHECK_SPARK_HOME)

# Dynamically load project root dir and jars.
project_root = os.getcwd() + "/.."
jars = run_cmd("ls %s/target/prep-buddy-?.?.?-jar-with-dependencies.jar" % project_root)

# Set environment variables.
os.environ["PYSPARK_SUBMIT_ARGS"] = "--jars %s --driver-class-path %s pyspark-shell" % (jars, jars)

# os.environ["SPARK_CONF_DIR"] = "%s/test/resources/conf" % os.getcwd()
