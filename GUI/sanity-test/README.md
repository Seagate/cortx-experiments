## Prerequisites

- Nodejs and npm are required for running the test cases. Download the project present in the 'rack' branch of cortx-management portal.
- Create a prod build with the command 'npm run build'. Build artifacts will be present inside the 'dist' folder.
- Run the command 'npx serve' from this 'dist' folder.
- This would start a server on the port 3000 and serves the project.
- Same set of test cases have been written using different test frameworks to explore them.

### Jest-puppeteer

- Navigate to the 'jest-puppeteer' folder and run the command 'npm i' to install the dependencies.
- Run the command 'npm test' to execute the test cases.

### Selenium webdriver + Jest

- Navigate to the 'selenium-webdriver-jest' folder and run the command 'npm i' to install the dependencies.
- Run the command 'npm test' to execute the test cases.

### Cypress

- Navigate to the 'cypress' folder and run the command 'npm i' to install the dependencies.
- Run the command 'npm test' to execute the test cases.
