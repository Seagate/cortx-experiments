describe("Presence of dashboard widgets", () => {
  before(() => {
    cy.visit("http://localhost:3000/");
  });

  it('Capacity widget"', () => {
    cy.get(".capacity-widget-container").should("contain", "Available");
  });

  it('Storage components widget"', () => {
    cy.get(".storage-components-widget-container").should("contain", "Buckets");
  });

  it('Performance widget"', () => {
    cy.get(".performance-widget-container").should(
      "contain",
      "Read Throughput"
    );
  });

  it('Cluster Health widget"', () => {
    cy.get(".health-widget-container").should("contain", "Online");
  });

  it('Alerts widget"', () => {
    cy.get(".alert-widget-container").should("contain", "Warning");
  });

  it('Background Activities widget"', () => {
    cy.get(".bg-activities-widget-container").should("contain", "Tasks");
  });
});
