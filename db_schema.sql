CREATE TABLE `user_reg_ai`.`new_table` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `new_tablecol` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `mobile` VARCHAR(45) NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);