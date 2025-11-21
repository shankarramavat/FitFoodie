-- Create the database (if your provider allows it, otherwise use the default one)
CREATE DATABASE IF NOT EXISTS geeklogin;
USE geeklogin;

-- Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id int auto_increment,
    username varchar(50),
    password varchar(255), -- Increased length for hashed passwords
    email varchar(100),
    PRIMARY KEY (id)
);

-- Create nutrients table
CREATE TABLE IF NOT EXISTS nutrients (
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
