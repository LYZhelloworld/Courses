CREATE TABLE `Professors` (
  `SSN` INT NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL COMMENT '',
  `age` INT NULL COMMENT '',
  `rank` VARCHAR(45) NULL COMMENT '',
  `specialty` VARCHAR(45) NULL COMMENT '',
  PRIMARY KEY (`SSN`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Projects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Projects` (
  `project_number` INT NOT NULL COMMENT '',
  `sponsor` VARCHAR(45) NULL COMMENT '',
  `starting_date` DATE NULL COMMENT '',
  `ending_date` DATE NULL COMMENT '',
  `budget` INT NULL COMMENT '',
  `supervised_by` INT NOT NULL COMMENT '',
  `managed_by` INT NOT NULL COMMENT '',
  PRIMARY KEY (`project_number`)  COMMENT '',
  INDEX `SSN_idx1` (`supervised_by` ASC)  COMMENT '',
  INDEX `SSN_idx` (`managed_by` ASC)  COMMENT '',
  CONSTRAINT `SSN`
    FOREIGN KEY (`supervised_by`)
    REFERENCES `mydb`.`Professors` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SSN`
    FOREIGN KEY (`managed_by`)
    REFERENCES `mydb`.`Professors` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Departments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Departments` (
  `dept_number` INT NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL COMMENT '',
  `main_office` VARCHAR(45) NULL COMMENT '',
  `dept_head` INT NOT NULL COMMENT '',
  PRIMARY KEY (`dept_number`)  COMMENT '',
  INDEX `SSN_idx` (`dept_head` ASC)  COMMENT '',
  CONSTRAINT `SSN`
    FOREIGN KEY (`dept_head`)
    REFERENCES `mydb`.`Professors` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Graduate_Students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Graduate_Students` (
  `SSN` INT NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL COMMENT '',
  `age` INT NULL COMMENT '',
  `degree_program` VARCHAR(45) NULL COMMENT '',
  `major_dept` INT NOT NULL COMMENT '',
  PRIMARY KEY (`SSN`)  COMMENT '',
  INDEX `dept_number_idx` (`major_dept` ASC)  COMMENT '',
  CONSTRAINT `dept_number`
    FOREIGN KEY (`major_dept`)
    REFERENCES `mydb`.`Departments` (`dept_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Prof_Works_on`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Prof_Works_on` (
  `prof_SSN` INT NOT NULL COMMENT '',
  `project_number` INT NOT NULL COMMENT '',
  INDEX `project_number_idx` (`project_number` ASC)  COMMENT '',
  CONSTRAINT `SSN`
    FOREIGN KEY (`prof_SSN`)
    REFERENCES `mydb`.`Professors` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `project_number`
    FOREIGN KEY (`project_number`)
    REFERENCES `mydb`.`Projects` (`project_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Students_Worked_on`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Students_Worked_on` (
  `SSN` INT NOT NULL COMMENT '',
  `project_number` INT NOT NULL COMMENT '',
  INDEX `SSN_idx` (`SSN` ASC)  COMMENT '',
  INDEX `project_number_idx` (`project_number` ASC)  COMMENT '',
  CONSTRAINT `SSN`
    FOREIGN KEY (`SSN`)
    REFERENCES `mydb`.`Graduate_Students` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `project_number`
    FOREIGN KEY (`project_number`)
    REFERENCES `mydb`.`Projects` (`project_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Department_Worked_in`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Department_Worked_in` (
  `department` INT NOT NULL COMMENT '',
  `SSN` INT NOT NULL COMMENT '',
  `time_percentage` FLOAT NULL COMMENT '',
  INDEX `SSN_idx` (`SSN` ASC)  COMMENT '',
  INDEX `dept_number_idx` (`department` ASC)  COMMENT '',
  CONSTRAINT `SSN`
    FOREIGN KEY (`SSN`)
    REFERENCES `mydb`.`Professors` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `dept_number`
    FOREIGN KEY (`department`)
    REFERENCES `mydb`.`Departments` (`dept_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Advisor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Advisor` (
  `Advisor` INT NOT NULL COMMENT '',
  `Advisee` INT NOT NULL COMMENT '',
  INDEX `SSN_idx` (`Advisor` ASC)  COMMENT '',
  INDEX `SSN_idx1` (`Advisee` ASC)  COMMENT '',
  CONSTRAINT `SSN`
    FOREIGN KEY (`Advisor`)
    REFERENCES `mydb`.`Graduate_Students` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SSN`
    FOREIGN KEY (`Advisee`)
    REFERENCES `mydb`.`Graduate_Students` (`SSN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
