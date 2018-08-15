-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`team_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`team_table` (
  `team_id` INT(11) NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`team_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`employee_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`employee_table` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `emp_name` VARCHAR(100) NOT NULL,
  `food_tag` VARCHAR(45) NOT NULL,
  `team_name` VARCHAR(45) NULL,
  `team_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_employee_table_team_table1_idx` (`team_id` ASC),
  CONSTRAINT `fk_employee_table_team_table1`
    FOREIGN KEY (`team_id`)
    REFERENCES `mydb`.`team_table` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`menu_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`menu_table` (
  `menu_id` INT(11) NOT NULL AUTO_INCREMENT,
  `item_name` VARCHAR(100) NULL DEFAULT NULL,
  `price` INT(11) NULL DEFAULT NULL,
  `category` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`menu_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`order_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`order_table` (
  `order_id` INT(11) NOT NULL AUTO_INCREMENT,
  `employee_id` INT(11) NULL DEFAULT NULL,
  `category` VARCHAR(45) NULL DEFAULT NULL,
  `order_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `menu_id` INT(11) NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_order_table_menu_table1_idx` (`menu_id` ASC),
  CONSTRAINT `fk_order_table_menu_table1`
    FOREIGN KEY (`menu_id`)
    REFERENCES `mydb`.`menu_table` (`menu_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`restaurant_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`restaurant_table` (
  `res_id` INT(11) NOT NULL AUTO_INCREMENT,
  `res_name` VARCHAR(145) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `menu_id` INT(11) NOT NULL,
  PRIMARY KEY (`res_id`),
  INDEX `fk_restaurant_table_menu_table1_idx` (`menu_id` ASC),
  CONSTRAINT `fk_restaurant_table_menu_table1`
    FOREIGN KEY (`menu_id`)
    REFERENCES `mydb`.`menu_table` (`menu_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

