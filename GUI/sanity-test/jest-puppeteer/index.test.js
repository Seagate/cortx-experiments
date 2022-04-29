describe("Presence of dashboard widgets", () => {
  beforeAll(async () => {
    await page.goto("http://localhost:3000");
  });

  it("Capacity widget", async () => {
    const capacityWidget = await page.$eval(
      ".capacity-widget-container",
      (input) => input.innerHTML
    );
    expect(capacityWidget).toContain("Available");
  });

  it("Storage components widget", async () => {
    const capacityWidget = await page.$eval(
      ".storage-components-widget-container",
      (input) => input.innerHTML
    );
    expect(capacityWidget).toContain("Buckets");
  });

  it("Performance widget", async () => {
    const capacityWidget = await page.$eval(
      ".performance-widget-container",
      (input) => input.innerHTML
    );
    expect(capacityWidget).toContain("Read Throughput");
  });

  it("Cluster health widget", async () => {
    const capacityWidget = await page.$eval(
      ".health-widget-container",
      (input) => input.innerHTML
    );
    expect(capacityWidget).toContain("Online");
  });

  it("Alerts widget", async () => {
    const capacityWidget = await page.$eval(
      ".alert-widget-container",
      (input) => input.innerHTML
    );
    expect(capacityWidget).toContain("Warning");
  });

  it("Background activities widget", async () => {
    const capacityWidget = await page.$eval(
      ".bg-activities-widget-container",
      (input) => input.innerHTML
    );
    expect(capacityWidget).toContain("Tasks");
  });
});

describe("Check navigation from dashboard", () => {
  beforeEach(async () => {
    await page.goto("http://localhost:3000");
  });

  it("Navigate to health page", async () => {
    const healthWidgetViewIcon = await page.$(
      ".health-widget-container .title-section .action-btn"
    );
    await healthWidgetViewIcon.click();
    await expect(page.url()).toContain("/health");
  });

  it("Navigate to alert page", async () => {
    const alertWidgetViewIcon = await page.$(
      ".alert-widget-container .title-section .action-btn"
    );
    await alertWidgetViewIcon.click();
    await expect(page.url()).toContain("/alerts");
  });
});
