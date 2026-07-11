# OrangeHRM Login Testing Project

## Overview

This project demonstrates Manual Testing and Selenium Automation Testing of the OrangeHRM Login module. It covers the complete Software Testing Life Cycle (STLC) for the login functionality, including test planning, test case design, execution, defect reporting, and automation.

The project was developed to gain hands-on experience in software testing tools and practices used in the QA industry.

---

## Objectives

- Perform Manual Testing of the OrangeHRM Login module.
- Design and execute login test cases.
- Identify and report defects using Jira.
- Automate login scenarios using Selenium WebDriver with Python.
- Compare expected and actual results during automation execution.

---

## Tools & Technologies

- Python
- Selenium WebDriver
- ChromeDriver
- Visual Studio Code
- Jira
- Microsoft Excel
- Google Chrome

---

## Project Structure

```
OrangeHRM-Login-Testing/
│
├── README.md
│
├── Manual Testing/
│   ├── OrangeHRM Test.xlsx
│   ├── OrangeHRM Testing Report.pdf
│   ├── Manual Testing Guide.txt
│   ├── login_page.png
│   ├── successful_login.png
│   └── Invalid_login.png
│
├── Selenium Automation/
│   ├── automation.py
│   ├── code_1.png
│   ├── code_2.png
│   ├── automation_1.png
│   ├── automation_2.png
│   ├── output_1.png
│   └── output_2.png
│
├── Bug Reports/
│   ├── Bug_001_Lowercase_Username_Report.docx
│   └── Bug_001.png
│
├── Jira/
    ├── Jira_Dashboard.png
    ├── Jira_List.png
```

---

## Manual Testing

The login module was tested using different input combinations.

### Test Scenarios

- Valid username and password
- Invalid username
- Invalid password
- Invalid username and password
- Blank username
- Blank password
- Blank username and password
- Username case sensitivity validation

**Total Test Cases:** 12

---

## Selenium Automation

The automation script performs the following steps:

- Launch Chrome Browser
- Open OrangeHRM Login Page
- Execute all login test cases
- Compare Expected vs Actual Results
- Display PASS/FAIL status
- Log out after successful login
- Detect application behavior differences

---

## Bug Report

### Bug ID
**BUG_001**

### Title
Username field accepts lowercase username (`admin`) and allows successful login.

### Expected Result
The application should reject login if username validation is case-sensitive.

### Actual Result
The application allows successful login using the lowercase username.

The defect has been documented with screenshots and reported in Jira.

---

## Jira

This project includes:

- Task Creation
- Bug Reporting
- Defect Tracking
- Attachments
- Screenshots
- Test Evidence

---

## Learning Outcomes

Through this project, I gained practical experience in:

- Manual Testing
- Test Case Design
- Decision Table Testing
- Bug Reporting
- Jira Workflow
- Selenium WebDriver
- Python Automation
- Explicit Waits
- Exception Handling
- Test Execution Reporting

---

## Author

**Kumar Suraj**

B.Tech Computer Science & Engineering

Aspiring Software QA Engineer | Manual Testing | Selenium Automation | Python | Jira