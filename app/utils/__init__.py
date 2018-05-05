def getHomeDir():
    from pathlib import Path
    return str(Path.home())


def getLinuxVersion():
    import subprocess as py_process
    from app.values.Constants import UNAME

    command_execution = py_process.run(UNAME.split(), stdout=py_process.PIPE)
    return command_execution.stdout.decode("utf-8")


def getCPUCount():
    from psutil import cpu_count
    return cpu_count()


def returnToHomeDir():
    import subprocess
    from app.values.Constants import GOTO_HOME

    subprocess.run(GOTO_HOME.split())
