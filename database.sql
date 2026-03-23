-- -----------------------------------------------------
-- Use and maintain this sql to create and update tables
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `Event` (nl = Gebeurtenis)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Event` (
                                       `event_id` INT NOT NULL AUTO_INCREMENT,
                                       `description` VARCHAR(100) NOT NULL,
    `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`event_id`)
    ) ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8mb4
    COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Dummy data in `Event` (nl = Gebeurtenis)
-- -----------------------------------------------------
INSERT INTO `Event`
(`description`, `date`)
VALUES ("dummy:button clicked", CURRENT_TIMESTAMP ),
       ("dummy:button clicked", CURRENT_TIMESTAMP );