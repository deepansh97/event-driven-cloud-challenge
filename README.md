# event-driven-cloud-challenge

Overview:
The main task of this challenge is to automate an AWS pipeline by using Python and AWS cloud services, more details on the same can be found here .

Steps which leads to problem solving:
1. ETL JOB : Created a CloudWatch event rule to trigger a Lambda function once in a day to perform the data transformation and load the data to PostgreSQL RDS database.

2. Extraction and transformation: In this step I have extracted the data from two CSV files using Python Pandas library and perform data manipulations in the python code:

Cleaning: The date field should be converted to a date object, not a string.
Joining: We want to show recovered cases as well as confirmed cases and deaths. The NYT data does not track recoveries, so needed to pull US recovery data from this Johns Hopkins dataset and merge it into the record for each day.
Filtering: Remove non-US data from the Johns Hopkins dataset. Remove any days that do not exist in both datasets.
3. Load: The lambda function loads the transformed data to the RDS PostgresSQL database. I tried to use DynamoDB but later realized that quicksight does not work with it so switched to postgres RDS DB instead.

4. Notification: Notifications have been configured on successfully completion of the ETL job and communicating the number of records inserted into the database daily in email. Any other failures or exceptions in Lambda code will also be notified using SNS topic and an email will be sent through SNS subscription.

5. Error handling: Error handling is one of the important part while executing the code as it does not interrupt the normal flow of the code. My code is able handle every kind of errors, few given below:

If there is issue in connecting with the database then the code will throw an error and the user will get to know with the help of SNS

If data is not created successfully then the code will raise an error.

And many more errors like these.

6. Infrastructure as a Code: I have made sure that the infrastructure is defined on code by using AWS cloudformation. This was one of the most challenging part for me as I never had used cloudformation before but finally ended up creating the cloudformation template and learned a lot.pic.PNG

7. CI/CD Pipeline and Source control: I have used Github for source control and Github actions to configure CI/CD pipeline so that the changes can be updated whenever a push action is performed.

8. Dashboard: I have used quicksight to generate the visualization of the US data.

Final Takeaways:
This task was very challenging and have learned a lot in the whole journey. My final takeaways from the challenge are:

I got to know cloudformation more deeply, got a good hands-on in the journey, explored more on it while coding the template.

I learned about CI/CD pipeline and implemented that using github actions as the concept was new for me.

To do a transformation and database connectivity, I used pandas and psycopg2 module of python. This module is not readily available in lambda. I have used lambda layers to add the modules.
