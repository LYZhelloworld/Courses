select `email` from `student`;
select distinct `email` from `student`;
select `name` from `student` order by `name` desc;
select `name` from `student` group by `name` having count(`name`) > 1;
select distinct `name` from `student`;
select `name` from `student` where exists (select * from `loan` where `loan`.`owner` = `student`.`email` and `loan`.`book` = '978-0262033848');
select `name` from `student` where `email` in (select `owner` from `copy` where `copy`.`copy` >= 1 and `copy`.`book` in (select `ISBN13` from `book` where `book`.`pages` > 100 and `book`.`title` like '%computer%'));
select sum(ceiling(`pages` / 2.0)) as `pages_needed` from `book` where `ISBN13` = '978-0262033848' or `ISBN13` = '978-0321295354';
select distinct `name` from `student` where `email` in (select `owner` from `copy` where `book` <> '978-0262033848');
select `name` from `student` where `email` in (select `borrower` from `loan` where `book` = '978-0262033848');
select `name` from `student` where `email` in (select `owner` from `copy` where `book` = '978-0262033848') union select `name` from `student` where `email` in (select `borrower` from `loan` where `book` = '978-0262033848');
select `name` from `student` where `email` in (select `owner` from `copy` where `book` = '978-0262033848') or `email` in (select `borrower` from `loan` where `book` = '978-0262033848');

truncate `loan`;
select `name` from `student` where `email` in (select `owner` from `copy` where `book` = '978-0262033848') union select `name` from `student` where `email` in (select `borrower` from `loan` where `book` = '978-0262033848');
select `name` from `student` where `email` in (select `owner` from `copy` where `book` = '978-0262033848') or `email` in (select `borrower` from `loan` where `book` = '978-0262033848');

# Recover data
# This is not part of the submission
insert into `loan` select * from `loan_backup`;