## Introduction

Credit card companies need to understand customer behavior to retain customers and ensure their satisfaction. Analyzing demographic characteristics can reveal insights into spending patterns and credit card usage.

In this project, I will analyze a dataset containing demographic information and credit card usage details. My goal is to identify distinct customer segments based on demographic factors and understand how these factors influence spending behavior, credit limit, and utilization ratio. By uncovering trends within each demographic segment, I aim to provide valuable insights for improved customer satisfaction and retention.

## Dataset

Download: [Kaggle](https://www.kaggle.com/datasets/thedevastator/predicting-credit-card-customer-attrition-with-m)

Data description:

| Field                     | Mapped Name (in Notebooks)| Description                                                                      | Data Type |
|---------------------------|-------------------------|----------------------------------------------------------------------------------|-----------|
| CLIENTNUM                 | client_id               | Unique identifier for each customer                                              | Integer   |
| Attrition_Flag            | churn_status            | Flag indicating whether or not the customer has churned out                      | Boolean   |
| Customer_Age              | age                     | Age of customer                                                                  | Integer   |
| Gender                    | gender                  | Gender of customer                                                               | String    |
| Dependent_count           | dependents              | Number of dependents that customer has                                           | Integer   |
| Education_Level           | education_level         | Education level of customer                                                      | String    |
| Marital_Status            | marital_status          | Marital status of customer                                                       | String    |
| Income_Category           | income_category         | Income category of customer                                                      | String    |
| Card_Category             | card_category           | Type of card held by customer                                                    | String    |
| Months_on_book            | months_on_book          | How long customer has been on the books                                          | Integer   |
| Total_Relationship_Count  | total_relationships     | Total number of relationships customer has with the credit card provider         | Integer   |
| Months_Inactive_12_mon    | months_inactive         | Number of months customer has been inactive in the last twelve months            | Integer   |
| Contacts_Count_12_mon     | contacts                | Number of contacts customer has had in the last twelve months                    | Integer   |
| Credit_Limit              | credit_limit            | Credit limit of customer                                                         | Integer   |
| Total_Revolving_Bal       | revolving_balance       | Total revolving balance of customer                                              | Integer   |
| Avg_Open_To_Buy           | available_credit        | Average open to buy ratio of customer                                            | Integer   |
| Total_Amt_Chng_Q4_Q1      | change_in_purchase_amt  | Total amount changed from quarter 4 to quarter 1                                 | Integer   |
| Total_Trans_Amt           | total_purchase_amt      | Total transaction amount                                                         | Integer   |
| Total_Trans_Ct            | total_purchase_ct       | Total transaction count                                                          | Integer   |
| Total_Ct_Chng_Q4_Q1       | change_in_purchase_ct   | Total count changed from quarter 4 to quarter 1                                  | Integer   |
| Avg_Utilization_Ratio     | credit_utilization      | Average utilization ratio of customer                                            | Integer   |
