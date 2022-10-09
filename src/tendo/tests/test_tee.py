
import os
from tendo.tee import quote_command, system, system2


def test_1():
    """No                       CMD      os.system()

        1  sort /?             ok          ok
        2  "sort" /?           ok          ok
        3  sort "/?"           ok          ok
        4  "sort" "/?"         ok         [bad]
        5  ""sort /?""         ok          [bad]
        6  "sort /?"          [bad]         ok
        7  "sort "/?""        [bad]         ok
        8 ""sort" "/?""       [bad]           ok
    """

    quotes = {
        'dir >nul': 'dir >nul',
        'cd /D "C:\\Program Files\\"': '"cd /D "C:\\Program Files\\""',
        'python -c "import os" dummy': '"python -c "import os" dummy"',
        'sort': 'sort',
    }

    # we fake the os name because we want to run the test on any platform
    save = os.name
    os.name = 'nt'

    for key, value in quotes.items():
        resulted_value = quote_command(key)
        assert value == resulted_value
        # ret = os.system(resulted_value)
        # if not ret==0:
        #    print("failed")
    os.name = save


def test_2():
    assert system(['python', '-V']) == 0


def test_3():
    assert system2(['python', '-V'])[0] == 0


def test_4():
    assert system(['python', '-c', "print('c c')"]) == 0
