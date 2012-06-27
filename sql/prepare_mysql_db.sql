/* create database */
CREATE DATABASE IF NOT EXISTS kvlite_test;
/* create user for kvlite_test */
CREATE USER 'kvlite_test'@'localhost' IDENTIFIED BY 'eixaaghiequ6ZeiBahn0';
/* add 'kvlite_test' user rights for 'kvlite_test' database */
GRANT ALL ON kvlite_test.* TO 'kvlite_test'@'localhost';

