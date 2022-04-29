const { Builder, By, Key, util } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");

async function test() {
  let options = new chrome.Options();
  let driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(options)
    .build();

  await driver.get("https://www.google.com");
  await driver.findElement(By.name("q")).sendKeys("Selenium", Key.RETURN);
  await driver.quit();
}
test();
