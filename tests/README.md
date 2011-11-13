# First run

the first time you run the extension tests you have to initialize the test environment

    python tests/runtests.py --gpo_bin=xxx --gpo_src=xxx --extension_src=xxx --init

Please provide your path the the `gpodder bin path`, your `gpodder source path` and your `extension script source path`.

The script create a sub directory with the test database and the test files


# Run your tests

from now on you can start the tests with (without the --init parameter)

    python tests/runtests.py --gpo_bin=xxx --gpo_src=xxx --extension_src=xxx


