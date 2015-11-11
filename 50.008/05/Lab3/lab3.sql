select sum(`copy`) from `copy`;

select `book`, sum(`copy`) from `copy` group by `book`;

select `book`, sum(`available`) from `copy` group by `book` having sum(`available`) in (select max(`sum_available`) from (select `book`, sum(`available`) as `sum_available` from `copy` group by `book`) as `sum`);

select `student`.`name` from `student` where `student`.`email` in (select `loan`.`borrower` from `loan` where `loan`.`book` in (select `book`.`ISBN13` from `book` where `book`.`authors` = 'Charles Dickens'));

select count(*) from `book` where `book`.`authors` = 'Charles Dickens';

select `student`.`name` from `student` where `student`.`email` in (select `loan`.`borrower` from `loan` where `loan`.`book` in (select `book`.`ISBN13` from `book` where `book`.`authors` = 'Charles Dickens') group by `loan`.`borrower` having count(distinct `loan`.`book`) = (select count(*) from `book` where `book`.`authors` = 'Charles Dickens'));

select `student`.`name` from `student` where not exists (select * from (select * from `book` where `book`.`authors` = 'Charles Dickens') as `c_d_books` where not exists (select * from `loan` where (`loan`.`borrower` = `student`.`email` and `loan`.`book` = `c_d_books`.`ISBN13`)));

select `student`.`name` from `student` where `student`.`email` in (select `loan`.`borrower` from `loan` where `loan`.`book` in (select `book`.`ISBN13` from `book` where `book`.`authors` = 'C. J. Date') group by `loan`.`borrower` having count(distinct `loan`.`book`) = (select count(*) from `book` where `book`.`authors` = 'C. J. Date'));
select `student`.`name` from `student` where not exists (select * from (select * from `book` where `book`.`authors` = 'C. J. Date') as `c_d_books` where not exists (select * from `loan` where (`loan`.`borrower` = `student`.`email` and `loan`.`book` = `c_d_books`.`ISBN13`)));

create view `ComputerScienceLoan` as select * from `loan` where `owner` in (select `student`.`email` from `student` where `department` = 'Computer Science');
create view `ComputerScienceCopy` as select * from `copy` where `owner` in (select `student`.`email` from `student` where `department` = 'Computer Science');

create trigger `loan_borrower` after update on `student` for each row update `loan` set `loan`.`borrower` = new.`email` where `loan`.`borrower` = old.`email`;