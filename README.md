"# Retail-Banking" 
                      Retail Management
1)We have created a flask web application on Bank Retail Management which aims to work for a new AccountExecutive as well as a general bank employee which is the cashier in carrying out various operations and functionalities which the user or the cashier aims to get respectively.
 
2)For The Account Executive Of A Bank:
a)First of all there will be a login page which will log on the executive to the site based on his/her username and password.
b)The username and the password are checked in the Customer table of the SQL database using the search column.If the username and password match correctly then the executive gets the access to the further functionalities.


The username and password for new account executive is: Username: John@1234 Password: John@1234
The username and password for cashier account is: Username: Jane@1234  Password: Jane@1234
Login with above username and password for viewing the functionalities.
The database details are as follows:
phpmyadmin: http://www.phpmyadmin.co/
HOSTNAME: sql12.freemysqlhosting.net
Username: sql12347847
Password: YJJDM7xe4J
Database Name: sql12347847
Tables are : Account, Customer, Timeline, TimelineAccount, userstore


c)The website also gives new account executives a chance to register customers with the website by filling up a form on our front end framework where they will enter details like custssnid,custname,age,add1,state,city which in turn creates a new record in the database under the customer table with the column name being create.If while registering with the webpage the custssnid already exists we get a message on the screen citing that the account already exists with the given ssnid.
d)Now we have various functionalities for the executive like show customer details based on his customerid or customersessionid which is unique id established randomly while setting up a connection.Depending on the former or latter,the page is redirected and checks if they match or not and if they do it redirects to the page and show executive information otherwise a message is displayed saying no account found.
e)We have another functionality which is updating the customerinformation which uses the update column in our Customer Table in our database. Here again we check the randomly generated customersessionid or the customerid and determine if account exists in the first place and if it does we update the customer information in the database.We also ask for a final confirmation for the update to be made by asking the customerr to enter all of his credentials once again so that it's cross verified that the update has to be made.This ensures a level of security in the website such that an unknown person who may just have the customerid does not modify the credentials.
f)We have another functionality which is deleting the executive information which uses the delete column in our Customer Table in our database.Here again we check the randomly generated customersessionid or the customerid and determine if account exists in the first place and if it does we delete the customer information in the database.We also ask for a final confirmation for the deletion to go ahead by asking the customer to enter all of his credentials once again so that it's cross verified that the deletion has to be made from a valid source.This ensures a level of security in the website such that an unknown person who may just have the customerid does not erase or delete the credentials.
g)Now once the executive has entered the cridentials and verified it,he is taken into a form asking him to enter his id,type of deposit and the cash amount which are then checked into the account table of the database,here customerid acts as primary key connecting the customer table and the account table.Along with the id,type and cash amount the transaction date and time is also recorded and stored in the account table in our database.If the customerid does not match in the existing schema of the database it shows that the customerid does not exist on the front end.
h)In the Account table we can delete the account by entering the Type of account and the customerid.The system checks with the database the account with the given cridentials and accordingly the deletion is made.Also a final confirmation is needed for the deletion to go ahead
i)We also have customerstatus and accountstatus functionality which displays all the details of the customer and account when prompted.

3)For the Cashier of the Bank:
a) Now cashier will enter his accountid or the customerid and accounttype which are cross checked with the account database. Once the things are checked and verified it takes the user to the account operations page which now gives it three options which are deposit,withdraw and transfer 
b)Deposit-During the deposit transaction the user is asked for a cash amount to be deposited into his account.In the mean time the transactionid and the date and time details are recorded and stored in the timeline table which stores and records all the transactions made.The balance column in the account table is added now with the cash amount and the old balance is now
added with the cash amount and updated.After this is done the message Deposit Succesful is displayed on the screen.
c)Withdraw-During the withdrawl transaction the user is asked for a cash amount to be withdrawn from his account.In the mean time the transactionid and the date and time details are recorded and stored in the timeline table which stores and records all the transactions made.The balance column in the account table is subtracted now with the cash amount and the old balance is now subtracted with the cash amount and updated.If the amount to be withdrawn is greater than the balance in the account it gives a message that not enough balance is there for the transaction to go ahead.After this is done the message withdrawl Succesful is displayed on the screen.
d)Transfer-There is also a functionality to transfer money to another person in the existing bank provided the cridentials match from the sender and receiver and also provided that there is sufficient balance available for the transfer.
e)Statement-There is also a functionality to get all the account statements in the bank for the previous transactions made which the cashier can use to see and authenticate the various transactions made.This ensures a high level of reliability in the system.


