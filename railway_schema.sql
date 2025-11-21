-- Railway Schema for FitFoodie
-- Copy and paste this entire file into Railway's Query editor

-- Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id int auto_increment,
    username varchar(50),
    password varchar(255),
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
