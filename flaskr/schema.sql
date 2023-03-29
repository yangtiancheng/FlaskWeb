drop table if exists user;
drop table if exists post;

create table user (
    id integer primary key AUTOINCREMENT,
    username text unique not null,
    password text unique not null,
    name text
);

create table post (
    id integer primary key AUTOINCREMENT,
    author_id integer not null,
    create_date timestamp not null default current_timestamp,
    title text not null,
    body text not null,
    content text not null,
    foreign key(author_id) references user(id)
);