-- MySQL dump 10.13  Distrib 5.6.46, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: webapp
-- ------------------------------------------------------
-- Server version	5.6.46-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `webapp`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `webapp` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `webapp`;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `body` text NOT NULL,
  `author` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_admin`
--

DROP TABLE IF EXISTS `user_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_admin` (
  `school_num` char(13) NOT NULL,
  `password` text NOT NULL,
  `rank` tinyint(1) NOT NULL,
  `name` text NOT NULL,
  `phone` char(11) NOT NULL,
  PRIMARY KEY (`school_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_admin`
--

LOCK TABLES `user_admin` WRITE;
/*!40000 ALTER TABLE `user_admin` DISABLE KEYS */;
INSERT INTO `user_admin` VALUES ('2018302180148','$5$rounds=535000$ki3RB0Jl/wJBv9MX$hNaUbA8QmaJck49Vrnj/cKYSsPvqbELMsVLf02Kq526',1,'袁寰宇','02768777110'),('2018302180149','$5$rounds=535000$WZMWkG6Xa2jLpvMQ$XO2tTSD6zS7kG728NmNBAPSk1K5qSbPu/URsl8PyF9D',1,'马陈军','15100088888'),('2018302180150','$5$rounds=535000$xj8Dt41ZyeZPueDW$zZXJy/X4L/pzhmS00vbgs2bU0Fz4pFm7zbofO9yk/R8',1,'小明','15100066667'),('2018302180162','$5$rounds=535000$/zdEczdN1SOqcx/8$Gsj9BBUKArp1SHPRrsyAvDbszw6ZOJvNPp.pYhPOqdC',1,'二娃','13224218803');
/*!40000 ALTER TABLE `user_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_data`
--

DROP TABLE IF EXISTS `user_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `school_num` char(13) NOT NULL,
  `temperature` float NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schoolid` (`school_num`),
  CONSTRAINT `schoolid` FOREIGN KEY (`school_num`) REFERENCES `user_admin` (`school_num`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_data`
--

LOCK TABLES `user_data` WRITE;
/*!40000 ALTER TABLE `user_data` DISABLE KEYS */;
INSERT INTO `user_data` VALUES (2,'2018302180150',36.4,'2020-05-22'),(15,'2018302180150',36.4,'2020-05-26'),(16,'2018302180162',39,'2020-05-26'),(17,'2018302180148',45,'2020-05-26'),(18,'2018302180162',35,'2020-05-27'),(21,'2018302180149',36.4,'2020-05-29');
/*!40000 ALTER TABLE `user_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `name` text NOT NULL,
  `email` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('1','1@qq.com','1234','$5$rounds=535000$R7E3L6wZZL7/O6Bg$hX0nq.0q.KT0ZDD/s3q2gRIX.J.KuKzb/Nn1L5jmPA5'),('123456','123456@qq.com','123456','$5$rounds=535000$r32KPO2QtdsmRcqv$bt.X2H2SKEP.sSGmvlHP2qd6wOFfaK0WxG5N97wxj38'),('12347','32396428764@qq.com','fdsqzx@mail.bccto.me','$5$rounds=535000$dJjXy6.AmSTfI3Qu$hP0oBO46AVy5lpP35wB9JlzR3rJtl2zaETx/pGa9Y04'),('12347','32396428764@qq.com','fdsqzx@mail.bccto.me','$5$rounds=535000$SCJuUsxk0fy1ADt/$UBlnL3goTj0DzIewMThLBVmS7oDwWW9TayPEShkJpz.'),('12347','32396428764@qq.com','fdsqzx@mail.bccto.me','$5$rounds=535000$UoVrDdCOsMG2PkaZ$Gr/WBtwbHBgwsgX4fyQ8rZHyxKhDMPMeUbSJq5Jga11'),('12347','32396428764@qq.com','fdsqzx@mail.bccto.me','$5$rounds=535000$8SEyiL2KmIJmRSEC$nPTU08jpCTMvCOc7F8h/XnLGkpXQzcDbZunymstKvgA'),('12347','32396428764@qq.com','fdsqzx@mail.bccto.me','$5$rounds=535000$Si3C1Vjvx4z8EsOi$AeDzbS0CtLTnplGVeEMudHjTX6ooVHlwymBofvOk4L4'),('hello','32396428764@qq.com','2018302180149','$5$rounds=535000$GUZZPurfK8y173OH$W23t5X1ofnq6BSseynTyS6JZPe8TlSYUMOcNY2ZJXp5'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$vZUFYA5Gt5lB4Qui$6uIwy2zEEyROCsKT/fN1V.TbRnQC2USiF8TIymuiiqD'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$ZKahZEgJNN8n1EDe$br21Mea1es9vc2Q3GAFrcjEBQHAPdkZbp.9Zzn4rSk0'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$ZkDqj2EVoISjc/kP$jUpE9G.gpiFisAwyUEOLtU.Z19Lp24Yi4sAQhLj6MA8'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$QsoWJZxp.zsXqDyQ$zMFzAV1v6qGAE9oxcXzRwYNcEFZCLsowi09AL/84e3B'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$TCl3gaNcJ6tdJN69$Duay6heQzCCnW.NdTVhVFFl7f7t2hxxgiDusOltyuOA'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$vm9ZmL2w.PjabBvk$WDJQqrkrErQwmac6ERAFO0Kfkwm0F7NqaqKahGxe34D'),('hello','32396428764@qq.com','2018302180149','$5$rounds=535000$gLjCCqtJ5.KisjzK$sOFPF.kqUsHIZs8KYnLpTCMFDuDkyMJoWswAnJU40l6'),('hello','32396428764@qq.com','2018302180149','$5$rounds=535000$59CVb/yknQTcad0v$bhSWDbA0sKGRZuVYXsLa/ZlR18MkpJEomBwiqDH8XAD'),('hello','32396428764@qq.com','2018302180149','$5$rounds=535000$f3JJCdOXJlP2ypa4$v2mjWHCD0iQfPF5jHWatH9bEjuThNJYlgRpK6TuRZn9'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$Hp0ZthjCFnbj/EBH$9LjacKXW7IE57YmWPR6M/wePyW30kbVwod3vtGEUOK1'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$1oZy9MtrXWDYrhd1$vrHNNLAfsMkzzTOSBj1KbPOK2IHu9K1DqI6BoEKsNLA'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$nF6VnVqnD.VonPdv$sBU6LZOSgTrpFLPfkUgpmDTQ.3fe168bhM0PPIwEuQA'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$Fecr0UHO1BIb3Zzj$4iZrmZnI7Mv0y9sVPEC2R4JbaQ/ibEDnsGQCzBBybS5'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$nAof2NolVXzk6viH$KYP3QZJdoqpC/pN/JJaFWwLDCHd/5DUfCPc2SC6jTA/'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$FpnxlCzGD3upbafy$hJchVKC8vv0zMgedwiL/3W3XkfvPTpHkxp6i.SOw2hA'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$3H0IL8ID2OFbf.Vb$D9hoD5.PGvf.ZCT6rjsUPMY6VGb0.jLmYvXhlkkd0L3'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$SmiKQbxKpCka0c.T$/WxrOcOJd6IOnb70lzfKMGNiL0h2gfNYIoyAClg0Ef6'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$4K7lhhH9RuUksMzQ$I1bZVLC4SwIeV6GMtLQtMXUuOwX9KhV9cmkv2MJjdzB'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$5hb248XL9OEqy9iC$BWPHn3KJLTL20o49LGa5Pncsh1GCFqEl633CUBoS3R5'),('123456','32396428764@qq.com','2018302180149','$5$rounds=535000$0j9iNXNnY9C83uVj$WhVRI7qpJpTCgCGJOSmIu2AdLIvOszp2PNVQddpE169');
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

-- Dump completed on 2020-05-29 22:51:53
