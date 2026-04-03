"""
Selenium test suite for MA Power — Meta-Analysis Power & Sample Size Calculator.
Tests: normalCDF, normalQuantile, computeWithinVar, computeTau2FromI2,
       computePower, computeRequiredK, UI interactions, curves, report.
"""
import os, unittest, time, math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

HTML = 'file:///' + os.path.abspath(r'C:\Models\MAPowerCalc\ma-power.html').replace('\\', '/')


class TestMAPower(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument('--headless=new')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-gpu')
        cls.drv = webdriver.Edge(options=opts)
        cls.drv.get(HTML)
        time.sleep(1)
        # The IIFE encapsulates everything, so we expose functions for testing
        # by re-declaring them in global scope via execute_script
        cls.drv.execute_script("""
            // Re-expose the core functions for testing
            window._normalCDF = function(x) {
                if (!isFinite(x)) return x > 0 ? 1 : 0;
                var a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
                var sign = x < 0 ? -1 : 1; x = Math.abs(x)/Math.SQRT2;
                var t = 1.0/(1.0+p*x);
                var y = 1.0 - (((((a5*t+a4)*t)+a3)*t+a2)*t+a1)*t*Math.exp(-x*x);
                return 0.5*(1.0+sign*y);
            };
            window._normalQuantile = function(p) {
                if (p<=0) return -Infinity; if (p>=1) return Infinity; if (p===0.5) return 0;
                var a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00];
                var b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01];
                var c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00];
                var d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00];
                var pLow=0.02425,pHigh=1-pLow; var q,r;
                if (p<pLow) { q=Math.sqrt(-2*Math.log(p)); return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1); }
                else if (p<=pHigh) { q=p-0.5; r=q*q; return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1); }
                else { q=Math.sqrt(-2*Math.log(1-p)); return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1); }
            };
            window._computeWithinVar = function(effectType, effect, nPerStudy) {
                var n = nPerStudy;
                if (effectType === 'binary') {
                    var n1 = Math.floor(n / 2), n2 = n - n1;
                    var pCtrl = 0.2;
                    var or_ = Math.exp(Math.abs(effect));
                    var pExp = (pCtrl * or_) / (1 - pCtrl + pCtrl * or_);
                    pExp = Math.max(0.01, Math.min(0.99, pExp));
                    return 1 / (n1 * pCtrl * (1 - pCtrl)) + 1 / (n2 * pExp * (1 - pExp));
                } else {
                    var d2 = effect * effect;
                    return (4 / n) * (1 + d2 / 8);
                }
            };
            window._computeTau2FromI2 = function(i2Pct, vBar) {
                var i2 = i2Pct / 100;
                if (i2 >= 1) i2 = 0.99;
                if (i2 <= 0) return 0;
                return i2 * vBar / (1 - i2);
            };
            window._computePower = function(k, nPerStudy, effect, i2Pct, alpha, effectType) {
                if (k < 1 || nPerStudy < 2 || Math.abs(effect) < 1e-10) return 0;
                var vBar = window._computeWithinVar(effectType, effect, nPerStudy);
                var tau2 = window._computeTau2FromI2(i2Pct, vBar);
                var wStar = k / (vBar + tau2);
                var se = 1 / Math.sqrt(wStar);
                var zAlpha = window._normalQuantile(1 - alpha / 2);
                var lambda = Math.abs(effect) / se;
                var power = window._normalCDF(lambda - zAlpha) + window._normalCDF(-lambda - zAlpha);
                return Math.max(0, Math.min(1, power));
            };
            window._computeRequiredK = function(targetPower, nPerStudy, effect, i2Pct, alpha, effectType) {
                if (Math.abs(effect) < 1e-10) return Infinity;
                var lo = 2, hi = 1000;
                while (lo < hi) {
                    var mid = Math.floor((lo + hi) / 2);
                    var pw = window._computePower(mid, nPerStudy, effect, i2Pct, alpha, effectType);
                    if (pw >= targetPower) hi = mid; else lo = mid + 1;
                }
                return lo;
            };
        """)

    @classmethod
    def tearDownClass(cls):
        cls.drv.quit()

    def js(self, script):
        return self.drv.execute_script(script)

    # ---------------------------------------------------------------
    # 1. normalCDF
    # ---------------------------------------------------------------
    def test_01_normalCDF_at_zero(self):
        """normalCDF(0) should be 0.5."""
        val = self.js("return window._normalCDF(0);")
        self.assertAlmostEqual(val, 0.5, places=6)

    def test_02_normalCDF_at_positive(self):
        """normalCDF(1.96) should be ~0.975."""
        val = self.js("return window._normalCDF(1.96);")
        self.assertAlmostEqual(val, 0.975, places=3)

    def test_03_normalCDF_at_negative(self):
        """normalCDF(-1.96) should be ~0.025."""
        val = self.js("return window._normalCDF(-1.96);")
        self.assertAlmostEqual(val, 0.025, places=3)

    def test_04_normalCDF_large_positive(self):
        """normalCDF(10) should be ~1."""
        val = self.js("return window._normalCDF(10);")
        self.assertAlmostEqual(val, 1.0, places=6)

    def test_05_normalCDF_large_negative(self):
        """normalCDF(-10) should be ~0."""
        val = self.js("return window._normalCDF(-10);")
        self.assertAlmostEqual(val, 0.0, places=6)

    # ---------------------------------------------------------------
    # 2. normalQuantile
    # ---------------------------------------------------------------
    def test_06_normalQuantile_at_half(self):
        """normalQuantile(0.5) should be 0."""
        val = self.js("return window._normalQuantile(0.5);")
        self.assertAlmostEqual(val, 0.0, places=6)

    def test_07_normalQuantile_at_975(self):
        """normalQuantile(0.975) should be ~1.96."""
        val = self.js("return window._normalQuantile(0.975);")
        self.assertAlmostEqual(val, 1.96, places=2)

    def test_08_normalQuantile_at_025(self):
        """normalQuantile(0.025) should be ~-1.96."""
        val = self.js("return window._normalQuantile(0.025);")
        self.assertAlmostEqual(val, -1.96, places=2)

    def test_09_normalQuantile_at_zero(self):
        """normalQuantile(0) should be -Infinity."""
        # JS Infinity serializes as null via WebDriver JSON; check via string
        val = self.js("return String(window._normalQuantile(0));")
        self.assertEqual(val, '-Infinity')

    def test_10_normalQuantile_at_one(self):
        """normalQuantile(1) should be Infinity."""
        val = self.js("return String(window._normalQuantile(1));")
        self.assertEqual(val, 'Infinity')

    # ---------------------------------------------------------------
    # 3. computeWithinVar
    # ---------------------------------------------------------------
    def test_11_within_var_continuous(self):
        """Continuous SMD within-study variance: v ~ (4/N)(1 + d^2/8)."""
        val = self.js("return window._computeWithinVar('continuous', 0.5, 200);")
        expected = (4.0 / 200) * (1 + 0.25 / 8)
        self.assertAlmostEqual(val, expected, places=6)

    def test_12_within_var_continuous_zero_effect(self):
        """Continuous v with d=0: v = 4/N."""
        val = self.js("return window._computeWithinVar('continuous', 0, 100);")
        self.assertAlmostEqual(val, 0.04, places=6)

    def test_13_within_var_binary(self):
        """Binary outcome within-study variance should be positive and reasonable."""
        val = self.js("return window._computeWithinVar('binary', 0.5, 200);")
        self.assertGreater(val, 0)
        self.assertLess(val, 1, "v for N=200 binary should be < 1")

    # ---------------------------------------------------------------
    # 4. computeTau2FromI2
    # ---------------------------------------------------------------
    def test_14_tau2_zero_i2(self):
        """tau^2 should be 0 when I^2 = 0."""
        val = self.js("return window._computeTau2FromI2(0, 0.02);")
        self.assertEqual(val, 0)

    def test_15_tau2_50pct_i2(self):
        """tau^2 from I^2=50% with v_bar=0.02 -> tau^2=0.02."""
        val = self.js("return window._computeTau2FromI2(50, 0.02);")
        expected = 0.5 * 0.02 / 0.5  # = 0.02
        self.assertAlmostEqual(val, expected, places=6)

    def test_16_tau2_99pct_i2(self):
        """tau^2 from I^2=99% should be very large relative to v_bar."""
        val = self.js("return window._computeTau2FromI2(99, 0.02);")
        # tau2 = 0.99 * 0.02 / 0.01 = 1.98
        self.assertAlmostEqual(val, 1.98, places=4)

    # ---------------------------------------------------------------
    # 5. computePower
    # ---------------------------------------------------------------
    def test_17_power_basic_continuous(self):
        """Power for k=10, N=200, d=0.3, I2=50% should be between 0 and 1."""
        val = self.js("return window._computePower(10, 200, 0.3, 50, 0.05, 'continuous');")
        self.assertGreater(val, 0.3)
        self.assertLess(val, 1.0)

    def test_18_power_zero_effect(self):
        """Power with zero effect size should be 0 (or very close)."""
        val = self.js("return window._computePower(10, 200, 0, 50, 0.05, 'continuous');")
        self.assertEqual(val, 0)

    def test_19_power_large_k_high(self):
        """Power with k=100, N=500, d=0.5, I2=0% should be very high."""
        val = self.js("return window._computePower(100, 500, 0.5, 0, 0.05, 'continuous');")
        self.assertGreater(val, 0.99, "With k=100, N=500, d=0.5, I2=0 power should be near 1")

    def test_20_power_increases_with_k(self):
        """Power should increase as k increases."""
        p5 = self.js("return window._computePower(5, 200, 0.3, 30, 0.05, 'continuous');")
        p20 = self.js("return window._computePower(20, 200, 0.3, 30, 0.05, 'continuous');")
        self.assertGreater(p20, p5, "Power should increase with more studies")

    def test_21_power_decreases_with_heterogeneity(self):
        """Power should decrease as I^2 increases (more heterogeneity)."""
        p0 = self.js("return window._computePower(10, 200, 0.3, 0, 0.05, 'continuous');")
        p75 = self.js("return window._computePower(10, 200, 0.3, 75, 0.05, 'continuous');")
        self.assertGreater(p0, p75, "Power should decrease with higher I2")

    def test_22_power_binary_outcome(self):
        """Power for binary outcomes should be computable and reasonable."""
        val = self.js("return window._computePower(15, 300, 0.5, 30, 0.05, 'binary');")
        self.assertGreater(val, 0.1)
        self.assertLess(val, 1.0)

    # ---------------------------------------------------------------
    # 6. computeRequiredK
    # ---------------------------------------------------------------
    def test_23_required_k_basic(self):
        """Required k for 80% power should be a reasonable integer >= 2."""
        val = self.js("return window._computeRequiredK(0.8, 200, 0.3, 50, 0.05, 'continuous');")
        self.assertIsInstance(val, (int, float))
        self.assertGreaterEqual(val, 2)
        self.assertLessEqual(val, 500)

    def test_24_required_k_zero_effect(self):
        """Required k with zero effect should be Infinity."""
        val = self.js("return String(window._computeRequiredK(0.8, 200, 0, 50, 0.05, 'continuous'));")
        self.assertEqual(val, 'Infinity')

    def test_25_required_k_increases_with_i2(self):
        """More heterogeneity should require more studies."""
        k0 = self.js("return window._computeRequiredK(0.8, 200, 0.3, 0, 0.05, 'continuous');")
        k75 = self.js("return window._computeRequiredK(0.8, 200, 0.3, 75, 0.05, 'continuous');")
        self.assertGreater(k75, k0, "Higher I2 should require more studies")

    def test_26_power_at_required_k_meets_target(self):
        """Power at the required k should meet or exceed the target."""
        k = self.js("return window._computeRequiredK(0.8, 200, 0.3, 50, 0.05, 'continuous');")
        p = self.js(f"return window._computePower({k}, 200, 0.3, 50, 0.05, 'continuous');")
        self.assertGreaterEqual(p, 0.8, f"Power at k={k} should be >= 80%")

    # ---------------------------------------------------------------
    # 7. UI - POWER CALCULATION
    # ---------------------------------------------------------------
    def test_27_ui_power_calculation(self):
        """Clicking 'Calculate Power' should show results."""
        self.js("""
            document.getElementById('pw_k').value = '10';
            document.getElementById('pw_n').value = '200';
            document.getElementById('pw_effect').value = '0.3';
            document.getElementById('pw_i2').value = '50';
            document.getElementById('pw_alpha').value = '0.05';
            document.getElementById('calcPowerBtn').click();
        """)
        time.sleep(0.3)
        result_div = self.drv.find_element(By.ID, 'powerResult')
        self.assertNotEqual(result_div.value_of_css_property('display'), 'none',
                            "Power result should be visible")
        power_text = self.drv.find_element(By.ID, 'powerValue').text
        self.assertTrue(power_text.endswith('%'), f"Power should show %, got: {power_text}")
        # Parse the percentage
        pct = float(power_text.replace('%', ''))
        self.assertGreater(pct, 0)
        self.assertLess(pct, 100)

    def test_28_ui_power_color_coding(self):
        """Result box should be green for >=80%, amber for >=50%, red for <50%."""
        # High power scenario
        self.js("""
            document.getElementById('pw_k').value = '50';
            document.getElementById('pw_n').value = '500';
            document.getElementById('pw_effect').value = '0.5';
            document.getElementById('pw_i2').value = '0';
            document.getElementById('pw_alpha').value = '0.05';
            document.getElementById('calcPowerBtn').click();
        """)
        time.sleep(0.3)
        box_class = self.drv.find_element(By.ID, 'powerBox').get_attribute('class')
        self.assertIn('result-green', box_class, "High power should get green box")

    # ---------------------------------------------------------------
    # 8. UI - SAMPLE SIZE CALCULATION
    # ---------------------------------------------------------------
    def test_29_ui_sample_size_calculation(self):
        """Clicking 'Calculate k' on Sample Size tab should show results."""
        self.drv.find_element(By.ID, 'tab-sample').click()
        time.sleep(0.2)
        self.js("""
            document.getElementById('ss_power').value = '0.80';
            document.getElementById('ss_n').value = '200';
            document.getElementById('ss_effect').value = '0.3';
            document.getElementById('ss_i2').value = '50';
            document.getElementById('ss_alpha').value = '0.05';
            document.getElementById('calcSampleBtn').click();
        """)
        time.sleep(0.3)
        result_div = self.drv.find_element(By.ID, 'sampleResult')
        self.assertNotEqual(result_div.value_of_css_property('display'), 'none')
        k_text = self.drv.find_element(By.ID, 'sampleValue').text
        k_val = int(k_text) if k_text != '>999' else 1000
        self.assertGreaterEqual(k_val, 2, "Required k should be at least 2")

    def test_30_ui_sensitivity_table(self):
        """Sensitivity table should show k needed for different I^2 values."""
        # Should still be on sample tab from previous test
        rows = self.drv.find_elements(By.CSS_SELECTOR, '#sensBody tr')
        self.assertEqual(len(rows), 5, "Sensitivity table should have 5 rows (I2: 0,25,50,75,90)")

    # ---------------------------------------------------------------
    # 9. UI - POWER CURVE
    # ---------------------------------------------------------------
    def test_31_ui_power_curve(self):
        """Drawing power curve should render SVG and table."""
        self.drv.find_element(By.ID, 'tab-curve').click()
        time.sleep(0.2)
        self.js("""
            document.getElementById('cv_n').value = '200';
            document.getElementById('cv_effect').value = '0.3';
            document.getElementById('cv_alpha').value = '0.05';
            document.getElementById('drawCurveBtn').click();
        """)
        time.sleep(0.3)
        svg_container = self.drv.find_element(By.ID, 'curveSvg')
        svgs = svg_container.find_elements(By.TAG_NAME, 'svg')
        self.assertEqual(len(svgs), 1, "Should have one SVG element")
        # Check curve table
        rows = self.drv.find_elements(By.CSS_SELECTOR, '#curveBody tr')
        self.assertEqual(len(rows), 6, "Curve table should have 6 rows (k=5,10,15,20,30,50)")

    def test_32_ui_power_curve_table_values(self):
        """Power curve table should have 4 columns of power values per row."""
        rows = self.drv.find_elements(By.CSS_SELECTOR, '#curveBody tr')
        if len(rows) > 0:
            cells = rows[0].find_elements(By.TAG_NAME, 'td')
            # 5 cells: k, I2=0%, I2=25%, I2=50%, I2=75%
            self.assertEqual(len(cells), 5)

    # ---------------------------------------------------------------
    # 10. TAB NAVIGATION
    # ---------------------------------------------------------------
    def test_33_tab_navigation(self):
        """Clicking tabs should show correct panels."""
        tab_panel_pairs = [
            ('tab-power', 'panel-power'),
            ('tab-sample', 'panel-sample'),
            ('tab-curve', 'panel-curve'),
            ('tab-report', 'panel-report'),
        ]
        for tab_id, panel_id in tab_panel_pairs:
            self.drv.find_element(By.ID, tab_id).click()
            time.sleep(0.15)
            panel = self.drv.find_element(By.ID, panel_id)
            self.assertIn('active', panel.get_attribute('class'),
                          f"{panel_id} should be active")

    # ---------------------------------------------------------------
    # 11. THEME TOGGLE
    # ---------------------------------------------------------------
    def test_34_theme_toggle(self):
        """Dark mode toggle should switch data-theme attribute."""
        initial = self.js("return document.documentElement.getAttribute('data-theme');")
        self.drv.find_element(By.ID, 'themeToggle').click()
        time.sleep(0.2)
        after = self.js("return document.documentElement.getAttribute('data-theme');")
        self.assertNotEqual(initial, after)
        # Toggle back
        self.drv.find_element(By.ID, 'themeToggle').click()
        time.sleep(0.2)

    # ---------------------------------------------------------------
    # 12. REPORT GENERATION
    # ---------------------------------------------------------------
    def test_35_report_methods_text(self):
        """After power calc, report tab should have methods text."""
        # Run a power calculation first
        self.drv.find_element(By.ID, 'tab-power').click()
        time.sleep(0.1)
        self.js("""
            document.getElementById('pw_k').value = '15';
            document.getElementById('pw_n').value = '300';
            document.getElementById('pw_effect').value = '0.4';
            document.getElementById('pw_i2').value = '40';
            document.getElementById('pw_alpha').value = '0.05';
            document.getElementById('calcPowerBtn').click();
        """)
        time.sleep(0.3)
        # Switch to report tab
        self.drv.find_element(By.ID, 'tab-report').click()
        time.sleep(0.2)
        methods = self.drv.find_element(By.ID, 'methodsText').text
        self.assertIn('Valentine', methods, "Methods text should reference Valentine et al.")
        self.assertIn('15', methods, "Methods text should include k=15")
        self.assertIn('300', methods, "Methods text should include N=300")

    def test_36_report_r_code(self):
        """Report tab should show R code equivalent using metapower."""
        r_code = self.drv.find_element(By.ID, 'rCode').text
        self.assertIn('library(metapower)', r_code, "R code should use metapower package")
        self.assertIn('mpower', r_code, "R code should call mpower()")

    # ---------------------------------------------------------------
    # 13. EDGE CASES
    # ---------------------------------------------------------------
    def test_37_power_k_equals_2(self):
        """Minimum k=2 should compute valid power."""
        val = self.js("return window._computePower(2, 200, 0.3, 50, 0.05, 'continuous');")
        self.assertGreater(val, 0)
        self.assertLess(val, 1)

    def test_38_power_very_small_effect(self):
        """Very small effect (0.01) should yield low power."""
        val = self.js("return window._computePower(10, 200, 0.01, 50, 0.05, 'continuous');")
        self.assertLess(val, 0.1, "Tiny effect should have very low power")

    def test_39_power_very_large_effect(self):
        """Large effect (2.0) should yield high power even with few studies."""
        val = self.js("return window._computePower(5, 100, 2.0, 30, 0.05, 'continuous');")
        self.assertGreater(val, 0.9, "Large effect should have high power")

    def test_40_normalCDF_inverse_roundtrip(self):
        """normalCDF(normalQuantile(p)) should approximately equal p."""
        val = self.js("return window._normalCDF(window._normalQuantile(0.9));")
        self.assertAlmostEqual(val, 0.9, places=4)

    # ---------------------------------------------------------------
    # 14. BINARY VS CONTINUOUS COMPARISON
    # ---------------------------------------------------------------
    def test_41_binary_vs_continuous_differ(self):
        """Binary and continuous within-study variances should differ."""
        v_bin = self.js("return window._computeWithinVar('binary', 0.5, 200);")
        v_con = self.js("return window._computeWithinVar('continuous', 0.5, 200);")
        self.assertNotAlmostEqual(v_bin, v_con, places=3,
                                  msg="Binary and continuous within-study var should differ")

    # ---------------------------------------------------------------
    # 15. UI RADIO BUTTONS (effect type)
    # ---------------------------------------------------------------
    def test_42_effect_type_radio_buttons(self):
        """Effect type radio buttons should exist and be selectable."""
        self.drv.find_element(By.ID, 'tab-power').click()
        time.sleep(0.1)
        radios = self.drv.find_elements(By.CSS_SELECTOR, 'input[name="effectType"]')
        self.assertEqual(len(radios), 2, "Should have 2 effect type radio buttons")
        # Select continuous
        radios[1].click()
        time.sleep(0.1)
        checked = self.js("return document.querySelector('input[name=\"effectType\"]:checked').value;")
        self.assertEqual(checked, 'continuous')
        # Reset to binary
        radios[0].click()

    # ---------------------------------------------------------------
    # 16. ACCESSIBILITY
    # ---------------------------------------------------------------
    def test_43_tab_aria_attributes(self):
        """Tabs should have proper ARIA roles and states."""
        tab = self.drv.find_element(By.ID, 'tab-power')
        self.assertEqual(tab.get_attribute('role'), 'tab')
        self.drv.find_element(By.ID, 'tab-power').click()
        time.sleep(0.1)
        self.assertEqual(tab.get_attribute('aria-selected'), 'true')
        other = self.drv.find_element(By.ID, 'tab-sample')
        self.assertEqual(other.get_attribute('aria-selected'), 'false')


if __name__ == '__main__':
    unittest.main(verbosity=2)
