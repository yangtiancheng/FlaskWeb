drop table if exists user;
drop table if exists post;

create table user (
    id integer primary key AUTOINCREMENT,
    username text unique not null,
    password text unique not null
);

create table post (
    id integer primary key AUTOINCREMENT,
    name text unique not null
);