const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());

const main = async () => {
  const wsChromeEndpointurl =
    "ws://127.0.0.1:9222/devtools/browser/6011cad9-60f5-45e9-80be-7aff7cb5e888";
  const userAgent =
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36";
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--ignore-certificate-errors"],
  });
  // connect({
  //   browserWSEndpoint: wsChromeEndpointurl,
  // });

  const page = await browser.newPage();
  await page.setUserAgent(userAgent);
  await page.goto(" https://appportal.intranet.pajak.go.id/portal");
  page.waitForTimeout(8000);
  await page.hover('//li[@style="z-index: 99;"]');
  await page.hover('//*[@id="smoothmenu1"]/ul/li[2]/ul/li[2]/a');
  await page.click('//span[@id="mpnharianrekon2022"]');
  page.waitForTimeout(8000);
  await page.screenshot({ path: "ss.jpeg", fullPage: true });
  // await waitForTimout(5000);

  await browser.close();
};

main().catch((err) => console.log(err));
