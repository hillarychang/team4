-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Travel_Log
-- -----------------------------------------------------
-- An app to help users track common expenses while traveling.
DROP SCHEMA IF EXISTS `Travel_Log` ;

-- -----------------------------------------------------
-- Schema Travel_Log
--
-- An app to help users track common expenses while traveling.
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Travel_Log` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `Travel_Log` ;

-- -----------------------------------------------------
-- Table `Travel_Log`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Travel_Log`.`user` ;

CREATE TABLE IF NOT EXISTS `Travel_Log`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Travel_Log`.`trips`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Travel_Log`.`trips` ;

CREATE TABLE IF NOT EXISTS `Travel_Log`.`trips` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(255) NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_trips_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_trips_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Travel_Log`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Travel_Log`.`cars`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Travel_Log`.`cars` ;

CREATE TABLE IF NOT EXISTS `Travel_Log`.`cars` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `trips_id` INT NOT NULL,
  `company` VARCHAR(45) NULL,
  `total_days` INT NULL,
  `cost` INT NULL,
  `start_date` DATE NULL,
  `end_date` DATE NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_cars_trips1_idx` (`trips_id` ASC) VISIBLE,
  CONSTRAINT `fk_cars_trips1`
    FOREIGN KEY (`trips_id`)
    REFERENCES `Travel_Log`.`trips` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Travel_Log`.`hotels`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Travel_Log`.`hotels` ;

CREATE TABLE IF NOT EXISTS `Travel_Log`.`hotels` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `trips_id` INT NOT NULL,
  `check_in` DATE NULL,
  `check_out` DATE NULL,
  `cost` INT NULL,
  `name` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_hotels_trips1_idx` (`trips_id` ASC) VISIBLE,
  CONSTRAINT `fk_hotels_trips1`
    FOREIGN KEY (`trips_id`)
    REFERENCES `Travel_Log`.`trips` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Travel_Log`.`flights`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Travel_Log`.`flights` ;

CREATE TABLE IF NOT EXISTS `Travel_Log`.`flights` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `trips_id` INT NOT NULL,
  `flight_number` INT NULL,
  `destination` VARCHAR(255) NULL,
  `departure` DATE NULL,
  `arrival` DATE NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_flights_trips1_idx` (`trips_id` ASC) VISIBLE,
  CONSTRAINT `fk_flights_trips1`
    FOREIGN KEY (`trips_id`)
    REFERENCES `Travel_Log`.`trips` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Travel_Log`.`trips_has_hotels`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Travel_Log`.`trips_has_hotels` ;

CREATE TABLE IF NOT EXISTS `Travel_Log`.`trips_has_hotels` (
  `trips_id` INT NOT NULL,
  `hotels_id` INT NOT NULL,
  PRIMARY KEY (`trips_id`, `hotels_id`),
  INDEX `fk_trips_has_hotels_hotels1_idx` (`hotels_id` ASC) VISIBLE,
  INDEX `fk_trips_has_hotels_trips_idx` (`trips_id` ASC) VISIBLE,
  CONSTRAINT `fk_trips_has_hotels_trips`
    FOREIGN KEY (`trips_id`)
    REFERENCES `Travel_Log`.`trips` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_trips_has_hotels_hotels1`
    FOREIGN KEY (`hotels_id`)
    REFERENCES `Travel_Log`.`hotels` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
