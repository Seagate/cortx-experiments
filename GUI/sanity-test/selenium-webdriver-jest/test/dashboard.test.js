const { Builder, By } = require("selenium-webdriver");

let driver;
describe("Presence of dashboard widgets", () => {
  beforeAll(async () => {
    driver = await new Builder().forBrowser("chrome").build();
    await driver.get("http://localhost:3000");
  }, 10000);

  it("Capacity widget", async () => {
    const capacityWidget = await driver
      .findElement(By.css(".capacity-widget-container"))
      .getText();
    expect(capacityWidget).toContain("Available");
  });

  it("Storage components widget", async () => {
    const widget = await driver
      .findElement(By.css(".storage-components-widget-container"))
      .getText();
    expect(widget).toContain("Buckets");
  });

  it("Performance widget", async () => {
    const widget = await driver
      .findElement(By.css(".performance-widget-container"))
      .getText();
    expect(widget).toContain("Read Throughput");
  });

  it("Cluster health widget", async () => {
    const widget = await driver
      .findElement(By.css(".health-widget-container"))
      .getText();
    expect(widget).toContain("Online");
  });

  it("Alerts widget", async () => {
    const widget = await driver
      .findElement(By.css(".alert-widget-container"))
      .getText();
    expect(widget).toContain("Warning");
  });

  it("Background activities widget", async () => {
    const widget = await driver
      .findElement(By.css(".bg-activities-widget-container"))
      .getText();
    expect(widget).toContain("Tasks");
  });
}, 10000);

describe("Check navigation from dashboard", () => {
  beforeEach(async () => {
    await driver.get("http://localhost:3000");
  });

  afterAll(async () => {
    await driver.quit();
  }, 15000);

  it("Navigate to health page", async () => {
    const healthWidgetViewIcon = await driver.findElement(
      By.css(".health-widget-container .title-section .action-btn")
    );
    await healthWidgetViewIcon.click();
    const url = await driver.getCurrentUrl();
    expect(url).toContain("/health");
  });

  it("Navigate to alert page", async () => {
    const healthWidgetViewIcon = await driver.findElement(
      By.css(".alert-widget-container .title-section .action-btn")
    );
    await healthWidgetViewIcon.click();
    const url = await driver.getCurrentUrl();
    expect(url).toContain("/alerts");
  });
}, 10000);
