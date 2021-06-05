from subprocess import run
from subprocess import PIPE
from xml.dom import minidom
from tabulate import tabulate


# executes a shell command
def execute(cmd=[], shell=False, timeout=5):
    return run(cmd, shell=shell, stdout=PIPE, stderr=PIPE, timeout=timeout)


# reads a file
def read(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text.strip()


# creates a pretty result report
def create_report(table):
    return tabulate(table, headers=['Exercise', 'Grade', 'Message'])


# checks alu.circ
def check_ALU():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ALU.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/ALU')
    if output == expected:
        return (25, 'passed', '')
    else:
        return (0, 'failed', '')


# checks regfile.circ
def check_rgf():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/regfile.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/regfile')
    if output == expected:
        return (25, 'passed', '')
    else:
        return (0, 'failed', '')


# checks cpu.circ
def check_cpu():
    grade = 0
    frac = 50 / 71
    wrong = 0
    count = 0
    # basic (arithmetic/logic/shifts/lui)
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/basic.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip().split('\n')
    expected = read('tests/expected/basic').split('\n')
    for (o, e) in zip(output, expected):
        o = o.strip()
        e = e.strip()
        if o == e:
            grade += frac
        else:
            wrong += 1
    # branches (beq/blt/bltu)
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/branches.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip().split('\n')
    expected = read('tests/expected/branches').split('\n')
    for (o, e) in zip(output, expected):
        o = o.strip()
        e = e.strip()
        if o == e:
            grade += frac
        else:
            wrong += 1
    # memory (sw/lb/lh/lw)
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/memory.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip().split('\n')
    expected = read('tests/expected/memory').split('\n')
    for (o, e) in zip(output, expected):
        o = o.strip()
        e = e.strip()
        if o == e:
            grade += frac
        else:
            wrong += 1
    # jump (jal/jalr)
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/jump.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip().split('\n')
    expected = read('tests/expected/jump').split('\n')
    for (o, e) in zip(output, expected):
        o = o.strip()
        e = e.strip()
        if o == e:
            grade += frac
        else:
            wrong += 1
    grade = round(grade)
    return (grade, 'passed' if wrong == 0 else 'some tests failed', '')



# checks proj 2
def proj2_logisim():
    alu_result = check_ALU()
    rgf_result = check_rgf()
    cpu_result = check_cpu()
    table = []
    table.append(('1. ALU', *alu_result[0: 2]))
    table.append(('2. Register File', *rgf_result[0: 2]))
    table.append(('3. CPU', *cpu_result[0: 2]))
    errors = alu_result[2]
    errors += '\n' + rgf_result[2]
    errors += '\n' + cpu_result[2]
    errors = errors.strip()
    grade = 0
    grade += alu_result[0]
    grade += rgf_result[0]
    grade += cpu_result[0]
    grade = min(round(grade), 100)
    report = create_report(table)
    if errors != '':
        report += '\n\nMore Info:\n\n' + errors
    print(report)
    print('\n=> Score: %d/100' % grade)


if __name__ == '__main__':
    proj2_logisim()
