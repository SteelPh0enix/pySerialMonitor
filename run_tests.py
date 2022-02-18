import unittest

TEST_CASES_DIRECTORIES = [
    "./tests/utils",
    "./tests/rest_server",
    "./tests/serialports_manager",
]

if __name__ == "__main__":
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.runner.TextTestRunner()

    for test_dir in TEST_CASES_DIRECTORIES:
        try:
            print(f"===== Looking for tests in {test_dir}... =====")
            tests = test_loader.discover(test_dir, "*_tests.py", ".")
            print("===== Running tests... =====")
            test_runner.run(tests)
        except ImportError as ex:
            print(f"An error occurred while tried to import test directory: {ex.msg}")
