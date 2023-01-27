from glob import glob
from re import search
from xml.etree import ElementTree
from requests import get, post
from json import dumps
from argparse import ArgumentParser


def main(project_name, release_name):
    get('http://localhost:8000/proj/OBJ-1', timeout=5)
    url = "http://localhost:8000/upload"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    test_cases_and_requirements = read_test_cases_and_requirements()
    results = {}
    for test_name, result in read_results().items():
        req = test_cases_and_requirements[test_name]['verifies']
        test_case = test_cases_and_requirements[test_name]['test_case']
        results[req] = {test_case: result}
    data = {
        'project_name': project_name,
        'release_name': release_name,
        'reqs': results
    }
    return post(url, data=dumps(data), headers=headers, timeout=5)


def read_test_cases_and_requirements():
    """
    This function collects all of Python test function and parses docstrings to get test case id and covered
    requirement id
    :return: dict of test functions names (key) and test case and requirement ids as dict value
    """
    test_case_requirements_map = {}

    for file in glob('test_*.py'):
        with open(file, mode='r', encoding='utf-8') as module:
            for test in module.read().split('def'):
                if test.strip().startswith('test__'):
                    test_case = search('(TestCase: )(.*)', test.strip())
                    verifies = search('(Verifies: )(.*)', test.strip())
                    test_case_name = test.strip().split('(')[0]
                    test_case_requirements_map[test_case_name] = {
                        'test_case': test_case.group(2),
                        'verifies': verifies.group(2)
                    }
    return test_case_requirements_map


def read_results():
    all_test_cases = {}
    for file in glob('*.xml'):
        tree = ElementTree.parse(file)
        root = tree.getroot()
        for testcase in root.iter('testcase'):
            all_test_cases[testcase.attrib['name']] = 'pass'
        for failure in root.iter('failure'):
            failed_test_case = search(r'(def )(.*)(\()', failure.text).group(2)
            all_test_cases[failed_test_case] = 'fail'
    return all_test_cases


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--project_name', required=True)
    parser.add_argument('--release_name', required=True)
    args = parser.parse_args()
    main(args.project_name, args.release_name)
