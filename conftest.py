def pytest_runtest_setup(item):
    print("pytest_runtest_setup")

def pytest_runtest_logreport(report):
    print(f'Log Report:{report}')

def pytest_sessionstart(session):
    print("pytest_session start")

def pytest_sessionfinish(session):
    print("pytest_session finish")

def pytest_collection_modifyitems(session, config, items):
    for item in items:
        print(f"pytest_collection_modify items{item}", item)

def pytest_collection_finish(session):
    print('pytest_collection_finish')