-- MariaDB dump 10.19  Distrib 10.5.12-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: michelinsocial
-- ------------------------------------------------------
-- Server version	10.5.12-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `restaurants`
--

DROP TABLE IF EXISTS `restaurants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurants` (
  `Codice_pk` varchar(20) NOT NULL,
  `Nome` varchar(50) NOT NULL,
  `Categoria` varchar(20) DEFAULT NULL,
  `Indirizzo` varchar(150) DEFAULT NULL,
  `Sito` varchar(70) DEFAULT NULL,
  `Telefono` varchar(16) DEFAULT NULL,
  `Immagine` varchar(300) DEFAULT NULL,
  `Longitudine` float DEFAULT NULL,
  `Latitudine` float DEFAULT NULL,
  `Ranking` float DEFAULT NULL,
  PRIMARY KEY (`Codice_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurants`
--

LOCK TABLES `restaurants` WRITE;
/*!40000 ALTER TABLE `restaurants` DISABLE KEYS */;
INSERT INTO `restaurants` VALUES ('1788391034730029','Farina del mio sacco','Deli','28, Via Saraceno, Centro cittadino, Giardino, Ferrara, Emilia-Romagna, 44121, Italia','https://www.farinadelmiosaccoferrara.it','0532474303','https://lh5.googleusercontent.com/p/AF1QipMnDendXP0WDteyJBU9ZdcdZ6kA4d4vg8nnepIc=w427-h240-k-no',11.6229,44.8329,7),('237766690','Pasticceria Chiurato','Bar','Pasticceria Chiurato, 50, Corso Mazzini, Marostica, Colceresa, Vicenza, Veneto, 36063, Italia','https://www.pasticceriachiurato.it/','042472134','https://lh5.googleusercontent.com/p/AF1QipM1IfwMmoRwQ375SmxLgIwab5I37MoB34Sh9Wda=w426-h240-k-no',11.656,45.7467,5),('3110887','Ristorante Pizzeria Lunaelaltro - Marostica','Italian Restaurant','Ristorante Pizzeria Lunaelaltro, 33, Corso della Ceramica, Marostica, Colceresa, Vicenza, Veneto, 36063, Italia','http://www.lunaelaltro.it','+390424478098','https://lh5.googleusercontent.com/p/AF1QipMUlnhZwJ5ENnmZFunVgKW4KDuzb7cfsqjEOjIw=w408-h271-k-no',11.6607,45.7369,5),('4706333','Al Saiso','Pub','2, Via Crestano Menarola, Angarano, Bassano del Grappa, Colceresa, Vicenza, Veneto, 31061, Italia','http://www.alsaiso.it','0424220819','https://lh5.googleusercontent.com/p/AF1QipPlitS1aCG7AxYkKEaNRjNE2AlLkZWvlbGUKyIw=w408-h271-k-no',11.7321,45.7675,5),('5608297','Roadhouse Restaurant','Steakhouse','Stazione Termini, Piazzale Sisto V, Esquilino, Municipio Roma I, Roma, Roma Capitale, Lazio, 00100, Italia','http://www.roadhouse.it/it/ristorante-roadhouse-roma-termini','+390648907344','https://www.google.com/maps/vt/pb=!1m5!1m4!1i8!2i272!3i189!4i128!2m2!1e1!3i928!3m9!2sit!3sit!5e1105!12m1!1e4!12m1!1e47!12m1!1e3!4e0!5m1!1e0!23i10203575!23i1381033!23i1368782!23i1368785!23i47025228!23i4592408!23i1375050!23i4536287',12.5029,41.9017,5),('742243027','Pizzeria L\'Angelo e il Diavolo','Pizza place','San Mango Piemonte, Salerno, Campania, 84132, Italia','https://www.pizzerialangeloeildiavolo.it','+39089281793','https://lh5.googleusercontent.com/p/AF1QipMxS3wYgWE9HM56kpoEEXyHXxs7wX_ywekwoaR8=w408-h306-k-no',14.8297,40.6995,5);
/*!40000 ALTER TABLE `restaurants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `Email` varchar(50) NOT NULL,
  `Username` varchar(20) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Foto` varchar(200) DEFAULT NULL,
  `Admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (' test.ecample@gmail.com','Test Name','7bcf9d89298f1bfae16fa02ed6b61908fd2fa8de45dd8e2153a3c47300765328','',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

DROP TABLE IF EXISTS `favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favorite` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `place_id` varchar(20) NOT NULL,
  date_created timestamp default now(), 
  date_updated timestamp default now() on update now(),
  PRIMARY KEY (`id`),
  FOREIGN KEY (user_id) REFERENCES users(Email),
  FOREIGN KEY (place_id) REFERENCES restaurants(Codice_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Dump completed on 2022-07-20 14:33:18