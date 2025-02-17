-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 04, 2021 at 02:41 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `passport`
--

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `number` varchar(15) NOT NULL,
  `number_alt` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `email_alt` varchar(100) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `first_contact_date` date DEFAULT NULL,
  `source` varchar(20) DEFAULT NULL,
  `referred_by` varchar(30) DEFAULT NULL,
  `process_type` varchar(20) DEFAULT NULL,
  `first_registration_of` varchar(30) DEFAULT NULL,
  `lead_type` varchar(20) DEFAULT NULL,
  `search_required` varchar(5) DEFAULT NULL,
  `assigned_to` varchar(30) DEFAULT NULL,
  `search_location` varchar(30) DEFAULT NULL,
  `search_taluka` varchar(30) DEFAULT NULL,
  `wa_group` varchar(5) DEFAULT NULL,
  `wa_group_name` varchar(30) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
CREATE TABLE IF NOT EXISTS `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `registration` text DEFAULT NULL,
  `to_register` text DEFAULT NULL,
  `document` text DEFAULT NULL,
  `document_of` text DEFAULT NULL,
  `name` text DEFAULT NULL,
  `place` text DEFAULT NULL,
  `date` date DEFAULT NULL,
  `registered_date` date DEFAULT NULL,
  `doc_available` text DEFAULT NULL,
  `doc_in_office` text DEFAULT NULL,
  `sac_date` date DEFAULT NULL,
  `a/t_date` date DEFAULT NULL,
  `translation_date` date DEFAULT NULL,
  `notary_date` date DEFAULT NULL,
  `collector_date` date DEFAULT NULL,
  `apostle_date` date DEFAULT NULL,
  `send_to_pt_date` date DEFAULT NULL,
  `doc_reached_pt` text DEFAULT NULL,
  `received_in_pt_date` date DEFAULT NULL,
  `submitted_date` date DEFAULT NULL,
  `concluded_date` date DEFAULT NULL,
  `doc_issue_date` date DEFAULT NULL,
  `reg_bill` text DEFAULT NULL,
  `submitted` text DEFAULT NULL,
  `attachment` text DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `billable` text DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `followup`
--

DROP TABLE IF EXISTS `followup`;
CREATE TABLE IF NOT EXISTS `followup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `followup_for` text DEFAULT NULL,
  `type` text DEFAULT NULL,
  `date` date DEFAULT NULL,
  `comments` text DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reminder`
--

DROP TABLE IF EXISTS `reminder`;
CREATE TABLE IF NOT EXISTS `reminder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `remind` text DEFAULT NULL,
  `current_case_stage` text DEFAULT NULL,
  `closed_by` text DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `user_type` int(11) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `password`, `user_type`, `created_at`, `updated_at`) VALUES
(9, '11Testing User', 'sass@test.com', 'Pass:1234', 1, '2020-12-29 18:46:46', '2020-12-29 18:48:18'),
(10, 'New Employee', 'emp@emp.com', 'emp', 1, '2020-12-29 18:46:46', '2020-12-29 18:46:46'),
(12, 'sasda', 'asddfs', 'sdffsd', 1, '2020-12-29 18:46:46', '2020-12-29 18:46:46'),
(13, 'From the API', 'No email', 'add pwd', 2, '2020-12-29 18:46:46', '2020-12-29 18:46:46'),
(14, 'From the API', 'No email', 'add pwd', 2, '2020-12-29 18:46:46', '2020-12-29 18:46:46'),
(15, 'UasdI', 'dsa', 'fs sfd', 1, '2020-12-29 18:46:46', '2020-12-29 18:46:46'),
(18, 'Joshua', 'dsa', 'test', 1, '2021-01-25 17:26:54', '2021-01-25 17:26:54');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
