/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.2    Database: RESTAURANTS
-- ------------------------------------------------------
-- Server version	11.5.2-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `ADDRESS`
--

DROP TABLE IF EXISTS `ADDRESS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ADDRESS` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `zip` varchar(25) NOT NULL,
  `country` varchar(2) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_ADDRESS_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ADDRESS`
--

LOCK TABLES `ADDRESS` WRITE;
/*!40000 ALTER TABLE `ADDRESS` DISABLE KEYS */;
INSERT INTO `ADDRESS` VALUES
(1,'Teststreet 1','Salzburg','5020','AT','2024-10-28 11:00:51',NULL);
/*!40000 ALTER TABLE `ADDRESS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GUEST_TABLE`
--

DROP TABLE IF EXISTS `GUEST_TABLE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GUEST_TABLE` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `table_number` varchar(255) NOT NULL,
  `seats` int(11) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_GUEST_TABLE_id` (`id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `GUEST_TABLE_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `RESTAURANT` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GUEST_TABLE`
--

LOCK TABLES `GUEST_TABLE` WRITE;
/*!40000 ALTER TABLE `GUEST_TABLE` DISABLE KEYS */;
INSERT INTO `GUEST_TABLE` VALUES
(1,'001',4,1,'2024-10-28 11:00:51',NULL),
(2,'002',2,1,'2024-10-28 11:00:51',NULL),
(3,'003',5,1,'2024-10-28 11:00:51',NULL);
/*!40000 ALTER TABLE `GUEST_TABLE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MENU`
--

DROP TABLE IF EXISTS `MENU`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MENU` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` float NOT NULL,
  `category` varchar(255) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_MENU_id` (`id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `MENU_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `RESTAURANT` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MENU`
--

LOCK TABLES `MENU` WRITE;
/*!40000 ALTER TABLE `MENU` DISABLE KEYS */;
INSERT INTO `MENU` VALUES
(1,'Menu1',9,'Starter',1,'2024-10-28 11:00:51',NULL),
(2,'Menu2',8,'Starter',1,'2024-10-28 11:00:51',NULL),
(3,'Menu3',7.5,'Starter',1,'2024-10-28 11:00:51',NULL),
(4,'Menu4',16,'Main Course',1,'2024-10-28 11:00:51',NULL),
(5,'Menu5',16,'Main Course',1,'2024-10-28 11:00:51',NULL),
(6,'Menu6',19,'Main Course',1,'2024-10-28 11:00:51',NULL),
(7,'Menu7',18.5,'Main Course',1,'2024-10-28 11:00:51',NULL),
(8,'Menu8',8.5,'Desert',1,'2024-10-28 11:00:51',NULL),
(9,'Menu9',9.5,'Desert',1,'2024-10-28 11:00:51',NULL),
(10,'Drink1',5,'Drinks',1,'2024-10-28 11:00:51',NULL),
(11,'Drink2',6,'Drinks',1,'2024-10-28 11:00:51',NULL);
/*!40000 ALTER TABLE `MENU` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REL_MENU_ORDER`
--

DROP TABLE IF EXISTS `REL_MENU_ORDER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `REL_MENU_ORDER` (
  `menu_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`menu_id`,`order_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `REL_MENU_ORDER_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `MENU` (`id`),
  CONSTRAINT `REL_MENU_ORDER_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `TABLE_ORDER` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REL_MENU_ORDER`
--

LOCK TABLES `REL_MENU_ORDER` WRITE;
/*!40000 ALTER TABLE `REL_MENU_ORDER` DISABLE KEYS */;
/*!40000 ALTER TABLE `REL_MENU_ORDER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REL_TABLE_RESERVATION`
--

DROP TABLE IF EXISTS `REL_TABLE_RESERVATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `REL_TABLE_RESERVATION` (
  `table_id` int(11) NOT NULL,
  `reservation_id` int(11) NOT NULL,
  PRIMARY KEY (`table_id`,`reservation_id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `REL_TABLE_RESERVATION_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `GUEST_TABLE` (`id`),
  CONSTRAINT `REL_TABLE_RESERVATION_ibfk_2` FOREIGN KEY (`reservation_id`) REFERENCES `RESERVATION` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REL_TABLE_RESERVATION`
--

LOCK TABLES `REL_TABLE_RESERVATION` WRITE;
/*!40000 ALTER TABLE `REL_TABLE_RESERVATION` DISABLE KEYS */;
/*!40000 ALTER TABLE `REL_TABLE_RESERVATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RESERVATION`
--

DROP TABLE IF EXISTS `RESERVATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RESERVATION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reservation_date` datetime NOT NULL,
  `time_from` time NOT NULL,
  `time_until` time NOT NULL,
  `people` int(11) NOT NULL,
  `reservation_name` varchar(255) NOT NULL,
  `reservation_number` varchar(10) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reservation_number` (`reservation_number`),
  UNIQUE KEY `ix_RESERVATION_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RESERVATION`
--

LOCK TABLES `RESERVATION` WRITE;
/*!40000 ALTER TABLE `RESERVATION` DISABLE KEYS */;
/*!40000 ALTER TABLE `RESERVATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RESTAURANT`
--

DROP TABLE IF EXISTS `RESTAURANT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RESTAURANT` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `open_from` time NOT NULL,
  `open_until` time NOT NULL,
  `open_days` varchar(255) NOT NULL,
  `address_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_RESTAURANT_id` (`id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `RESTAURANT_ibfk_1` FOREIGN KEY (`address_id`) REFERENCES `ADDRESS` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RESTAURANT`
--

LOCK TABLES `RESTAURANT` WRITE;
/*!40000 ALTER TABLE `RESTAURANT` DISABLE KEYS */;
INSERT INTO `RESTAURANT` VALUES
(1,'The Restaurant Name','10:00:00','22:00:00','TUESDAY;WEDNESDAY;THURSDAY;FRIDAY;SATURDAY;SUNDAY',1,'2024-10-28 11:00:51',NULL);
/*!40000 ALTER TABLE `RESTAURANT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TABLE_ORDER`
--

DROP TABLE IF EXISTS `TABLE_ORDER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TABLE_ORDER` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total` float NOT NULL,
  `waiter` varchar(255) NOT NULL,
  `table_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_TABLE_ORDER_id` (`id`),
  KEY `table_id` (`table_id`),
  CONSTRAINT `TABLE_ORDER_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `GUEST_TABLE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TABLE_ORDER`
--

LOCK TABLES `TABLE_ORDER` WRITE;
/*!40000 ALTER TABLE `TABLE_ORDER` DISABLE KEYS */;
/*!40000 ALTER TABLE `TABLE_ORDER` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-10-28 12:03:31
