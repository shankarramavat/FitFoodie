# Fit-Foodie

# Fit-Foodie

A user-interactive full stack web application that provides nutrition value of food.
It accepts food photographs as input, automatically recognizes the food and outputs the nutritional information.
It also shows user there history. So that they can track their intake of each nutrient

Some Screenshots of website are attached below
Home page. It has option to scan the food:
:![Home page](https://user-images.githubusercontent.com/85441257/218382738-6b320d25-f400-4a61-9d75-c8855634fb83.png)

About us ![Home page2](https://user-images.githubusercontent.com/85441257/218383005-04429b2e-b0f0-4077-bba5-6b9dfe73b42b.png)

Here you can select file to be uploaded
![Upload page](https://user-images.githubusercontent.com/85441257/218383036-f616ba1e-0e37-4937-87e7-4dfa66c1e989.png)

It shows nutritional value of scanned food
![Nutritional value](https://user-images.githubusercontent.com/85441257/218383152-7d74018b-5cd8-40d4-bda6-438ee11e3ece.png)

All the values displayed are in milligrams:
![Dashboard](https://user-images.githubusercontent.com/85441257/218383218-e3621e10-cd97-4936-9971-9fe002a53be8.png)

Schema for the project:
![Schema](https://user-images.githubusercontent.com/85441257/218472406-07bca278-9036-474d-9a5a-20a98c88907e.png)

## For local setup follow the following steps :

Open mysql command line client and follow the following steps.
Paste following commands.

create database geeklogin;

use geeklogin;

create table accounts
(  
 id int auto_increment,
username varchar(50),
password varchar(60),
email varchar(100),
PRIMARY KEY (ID)
);

create table nutrients (
fid int PRIMARY KEY auto_increment,
fname varchar(100),
u_id int,
fat float,
carbohydrates float,
cholesterol float,
protein float,
sodium float,
time Date default (CURRENT_DATE) not null,
FOREIGN KEY (u_id) references accounts(id)
);

create a .env file in the same directory and add your mysql password with the attribute "MYSQL_PASS"

run following command in your terminal:
pip install -r requirements.txt

# A video demonstration link of the project is provided below ;) :

link -> https://drive.google.com/file/d/1E7Gy9IPJ84IK6DiJ3y_U72G87xlQiPTU/view?usp=share_link
