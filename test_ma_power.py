"""
MA Power — Meta-Analysis Power & Sample Size Calculator
Selenium Test Suite: 25 tests
Run: python test_ma_power.py
"""
import sys, os, time, io, unittest
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ma-power.html')
URL = 'file:///' + HTML_PATH.replace('\\', '/')


def get_driver():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1400,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(2)
    return driver


class MAPowerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.driver.get(URL)
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        logs = cls.driver.get_log('browser')
        severe = [l for l in logs if l['level'] == 'SEVERE' and 'favicon' not in l.get('message', '')]
        if severe:
            print(f"\nJS ERRORS ({len(severe)}):")
            for l in severe:
                print(f"  {l['message']}")
        cls.driver.quit()

    def _reload(self):
        self.driver.get(URL)
        time.sleep(0.3)

    def _click(self, by, val):
        el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((by, val)))
        self.driver.execute_script("arguments[0].click()", el)
        return el

    def _set_input(self, input_id, value):
        el = self.driver.find_element(By.ID, input_id)
        el.clear()
        el.send_keys(str(value))

    # ─── 1. PAGE LOAD ───
    def test_01_page_loads(self):
        self.assertIn('MA Power', self.driver.title)

    def test_02_hero_visible(self):
        hero = self.driver.find_element(By.CSS_SELECTOR, '.hero-title')
        self.assertIn('MA Power', hero.text)

    def test_03_four_tabs(self):
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '.tab-btn')
        self.assertEqual(len(tabs), 4)

    def test_04_tab_labels(self):
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '.tab-btn')
        labels = [t.text for t in tabs]
        self.assertIn('1. Power', labels)
        self.assertIn('2. Sample Size', labels)
        self.assertIn('3. Power Curve', labels)
        self.assertIn('4. Report', labels)

    # ─── 2. POWER CALCULATION ───
    def test_05_power_default_inputs(self):
        """Default inputs are pre-filled."""
        self._reload()
        k = self.driver.find_element(By.ID, 'pw_k').get_attribute('value')
        self.assertEqual(k, '10')

    def test_06_calculate_power(self):
        """Clicking calculate shows power result."""
        self._reload()
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        result = self.driver.find_element(By.ID, 'powerResult')
        self.assertTrue(result.is_displayed())

    def test_07_power_value_displayed(self):
        """Power value is a percentage."""
        self._reload()
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        val = self.driver.find_element(By.ID, 'powerValue').text
        self.assertIn('%', val)

    def test_08_power_increases_with_k(self):
        """More studies = higher power."""
        self._reload()
        self._set_input('pw_k', '5')
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        pw5 = float(self.driver.find_element(By.ID, 'powerValue').text.replace('%', ''))

        self._set_input('pw_k', '30')
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        pw30 = float(self.driver.find_element(By.ID, 'powerValue').text.replace('%', ''))
        self.assertGreater(pw30, pw5)

    def test_09_power_decreases_with_i2(self):
        """Higher heterogeneity = lower power."""
        self._reload()
        self._set_input('pw_i2', '0')
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        pw0 = float(self.driver.find_element(By.ID, 'powerValue').text.replace('%', ''))

        self._set_input('pw_i2', '75')
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        pw75 = float(self.driver.find_element(By.ID, 'powerValue').text.replace('%', ''))
        self.assertGreater(pw0, pw75)

    def test_10_power_details_shown(self):
        """Power details show tau² and SE."""
        self._reload()
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        details = self.driver.find_element(By.ID, 'powerDetails').text
        self.assertIn('tau', details)
        self.assertIn('Pooled SE', details)

    def test_11_power_color_coding(self):
        """Result box is green for high power, red for low."""
        self._reload()
        self._set_input('pw_k', '50')
        self._set_input('pw_effect', '0.5')
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        box = self.driver.find_element(By.ID, 'powerBox')
        self.assertIn('result-green', box.get_attribute('class'))

    # ─── 3. SAMPLE SIZE ───
    def test_12_sample_size_calc(self):
        """Sample size calculation returns a number."""
        self._click(By.ID, 'tab-sample')
        time.sleep(0.2)
        self._click(By.ID, 'calcSampleBtn')
        time.sleep(0.3)
        result = self.driver.find_element(By.ID, 'sampleResult')
        self.assertTrue(result.is_displayed())
        val = self.driver.find_element(By.ID, 'sampleValue').text
        self.assertTrue(val.isdigit() or val == '>999')

    def test_13_sensitivity_table(self):
        """Sensitivity table shows k for different I² values."""
        self._click(By.ID, 'tab-sample')
        time.sleep(0.2)
        self._click(By.ID, 'calcSampleBtn')
        time.sleep(0.3)
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#sensBody tr')
        self.assertEqual(len(rows), 5)  # 5 I² levels

    def test_14_larger_effect_needs_fewer_studies(self):
        """Larger effect size requires fewer studies."""
        self._click(By.ID, 'tab-sample')
        time.sleep(0.2)
        self._set_input('ss_effect', '0.2')
        self._click(By.ID, 'calcSampleBtn')
        time.sleep(0.3)
        k_small = self.driver.find_element(By.ID, 'sampleValue').text

        self._set_input('ss_effect', '0.8')
        self._click(By.ID, 'calcSampleBtn')
        time.sleep(0.3)
        k_large = self.driver.find_element(By.ID, 'sampleValue').text

        k1 = 1000 if k_small == '>999' else int(k_small)
        k2 = 1000 if k_large == '>999' else int(k_large)
        self.assertGreater(k1, k2)

    # ─── 4. POWER CURVE ───
    def test_15_power_curve_renders(self):
        """Power curve tab renders SVG."""
        self._click(By.ID, 'tab-curve')
        time.sleep(0.2)
        self._click(By.ID, 'drawCurveBtn')
        time.sleep(0.5)
        svg_html = self.driver.find_element(By.ID, 'curveSvg').get_attribute('innerHTML')
        self.assertIn('path', svg_html)

    def test_16_curve_has_four_lines(self):
        """Power curve shows 4 I² lines."""
        self._click(By.ID, 'tab-curve')
        time.sleep(0.2)
        self._click(By.ID, 'drawCurveBtn')
        time.sleep(0.5)
        svg_html = self.driver.find_element(By.ID, 'curveSvg').get_attribute('innerHTML')
        # 4 curves + grid lines, so many paths. Check legend text
        self.assertIn('I', svg_html)
        self.assertIn('0%', svg_html)
        self.assertIn('75%', svg_html)

    def test_17_curve_table(self):
        """Power curve table shows data for key k values."""
        self._click(By.ID, 'tab-curve')
        time.sleep(0.2)
        self._click(By.ID, 'drawCurveBtn')
        time.sleep(0.5)
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#curveBody tr')
        self.assertEqual(len(rows), 6)  # k = 5, 10, 15, 20, 30, 50

    # ─── 5. TAB NAVIGATION ───
    def test_18_tab_click(self):
        """Clicking tabs switches panels."""
        self._click(By.ID, 'tab-report')
        time.sleep(0.2)
        panel = self.driver.find_element(By.ID, 'panel-report')
        self.assertIn('active', panel.get_attribute('class'))

    def test_19_tab_keyboard(self):
        """Arrow keys navigate tabs."""
        self._reload()
        tab = self.driver.find_element(By.ID, 'tab-power')
        tab.send_keys(Keys.ARROW_RIGHT)
        time.sleep(0.2)
        sample_tab = self.driver.find_element(By.ID, 'tab-sample')
        self.assertEqual(sample_tab.get_attribute('aria-selected'), 'true')

    # ─── 6. DARK MODE ───
    def test_20_dark_mode(self):
        """Dark mode toggle works."""
        self._reload()
        btn = self.driver.find_element(By.ID, 'themeToggle')
        self.driver.execute_script("arguments[0].click()", btn)
        time.sleep(0.2)
        theme = self.driver.find_element(By.TAG_NAME, 'html').get_attribute('data-theme')
        self.assertEqual(theme, 'dark')
        self.driver.execute_script("arguments[0].click()", btn)

    # ─── 7. REPORT TAB ───
    def test_21_methods_text_generated(self):
        """Methods text is generated after calculation."""
        self._reload()
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        self._click(By.ID, 'tab-report')
        time.sleep(0.2)
        methods = self.driver.find_element(By.ID, 'methodsText').text
        self.assertIn('Valentine', methods)
        self.assertIn('power', methods.lower())

    def test_22_r_code_generated(self):
        """R code references metapower package."""
        self._reload()
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        self._click(By.ID, 'tab-report')
        time.sleep(0.2)
        rcode = self.driver.find_element(By.ID, 'rCode').text
        self.assertIn('metapower', rcode)
        self.assertIn('mpower', rcode)

    # ─── 8. EFFECT TYPE TOGGLE ───
    def test_23_binary_effect_type(self):
        """Binary outcome is default selection."""
        self._reload()
        binary = self.driver.find_element(By.CSS_SELECTOR, 'input[name="effectType"][value="binary"]')
        self.assertTrue(binary.is_selected())

    def test_24_continuous_effect_type(self):
        """Switching to continuous works."""
        self._reload()
        continuous = self.driver.find_element(By.CSS_SELECTOR, 'input[name="effectType"][value="continuous"]')
        self.driver.execute_script("arguments[0].click()", continuous)
        self._click(By.ID, 'calcPowerBtn')
        time.sleep(0.3)
        details = self.driver.find_element(By.ID, 'powerDetails').text
        self.assertIn('SMD', details)

    # ─── 9. REFERENCES ───
    def test_25_references_present(self):
        """Report tab shows references."""
        self._click(By.ID, 'tab-report')
        time.sleep(0.2)
        text = self.driver.find_element(By.ID, 'panel-report').text
        self.assertIn('Valentine', text)
        self.assertIn('Jackson', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
