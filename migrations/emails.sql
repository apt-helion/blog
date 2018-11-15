# ************************************************************
# Sequel Pro SQL dump
# Version 5425
#
# https://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 165.227.57.12 (MySQL 5.5.60-MariaDB)
# Database: blog
# Generation Time: 2018-11-15 22:30:29 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table EmailLogs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `EmailLogs`;

CREATE TABLE `EmailLogs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `error` varchar(512) NOT NULL DEFAULT ' ',
  `email` varchar(256) NOT NULL DEFAULT ' ',
  `process` varchar(24) NOT NULL DEFAULT ' ',
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table Emails
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Emails`;

CREATE TABLE `Emails` (
  `email` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT ' ',
  `unsubscribe` varchar(36) NOT NULL DEFAULT ' ',
  `created` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table EmailVerifications
# ------------------------------------------------------------

DROP TABLE IF EXISTS `EmailVerifications`;

CREATE TABLE `EmailVerifications` (
  `code` varchar(36) NOT NULL DEFAULT '',
  `email` varchar(246) NOT NULL DEFAULT ' ',
  `expiry` datetime NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
