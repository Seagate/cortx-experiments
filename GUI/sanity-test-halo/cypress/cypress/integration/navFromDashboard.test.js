describe("Navigate from dashboard widgets", () => {
  beforeEach(() => {
    cy.visit("http://localhost:3000/");
  });

  it('Navigate to health page"', () => {
    cy.get(".health-widget-container .title-section .action-btn").click();
    cy.url().should("include", "/health");
  });

  it('Navigate to alerts page"', () => {
    cy.get(".alert-widget-container .title-section .action-btn").click();
    cy.url().should("include", "/alerts");
  });
});
