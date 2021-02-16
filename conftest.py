import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

project_path = Path(__file__).resolve().parent
DEFAULT_CHROMEDRIVER_PATH = project_path / 'chromedriver'
ADDBLOCK_PLUS_PATH = project_path / '3.10.2_0'


def pytest_addoption(parser):
    """Parses command line args"""
    parser.addoption(
        '--driver', action='store', default='chrome', help="Choose browser: chrome only"
    )
    parser.addoption(
        '--chromedriver_path',
        action='store',
        default=DEFAULT_CHROMEDRIVER_PATH,
        help="Path to chromedriver",
    )


@pytest.fixture(scope="function")
def driver(request):
    """Fixture creates driver"""
    browser_name = request.config.getoption("driver")
    chromedriver_path = request.config.getoption("chromedriver_path")
    if browser_name == "chrome":
        print("\nstart browser chrome for test...")
        options = Options()
        options.add_argument('load-extension=' + ADDBLOCK_PLUS_PATH.as_posix())
        driver = webdriver.Chrome(chromedriver_path, options=options)
    else:
        raise NotImplementedError(f"Browser {browser_name} is not implemented")
    yield driver
    print("\nquit browser...")
    driver.quit()
