-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 08, 2021 at 12:40 PM
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
CREATE DATABASE IF NOT EXISTS `passport` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `passport`;

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE `client` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `number` varchar(15) NOT NULL,
  `number_alt` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `email_alt` varchar(100) DEFAULT NULL,
  `location` varchar(50) NOT NULL,
  `first_contact_date` datetime NOT NULL,
  `source` varchar(20) NOT NULL,
  `referred_by` varchar(30) NOT NULL,
  `process_type` varchar(20) NOT NULL,
  `first_registration_of` varchar(30) NOT NULL,
  `lead_type` varchar(20) NOT NULL,
  `search_required` tinyint(1) NOT NULL,
  `assigned_to` varchar(30) NOT NULL,
  `search_location` varchar(30) NOT NULL,
  `search_taluka` varchar(30) NOT NULL,
  `wa_group` tinyint(1) NOT NULL,
  `wa_group_name` varchar(30) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
CREATE TABLE `document` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `registration` text NOT NULL,
  `to_register` text NOT NULL,
  `document` text NOT NULL,
  `document_of` text NOT NULL,
  `name` text NOT NULL,
  `place` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `registered_date` datetime NOT NULL DEFAULT current_timestamp(),
  `doc_available` text NOT NULL,
  `doc_in_office` text NOT NULL,
  `sac_date` datetime NOT NULL,
  `a/t_date` datetime NOT NULL,
  `translation_date` datetime NOT NULL,
  `notary_date` datetime NOT NULL,
  `collector_date` datetime NOT NULL,
  `apostle_date` datetime NOT NULL,
  `send_to_pt_date` datetime NOT NULL,
  `doc_reached_pt` datetime NOT NULL,
  `received_in_pt_date` datetime NOT NULL,
  `submitted_date` datetime NOT NULL,
  `concluded_date` datetime NOT NULL,
  `submitted` text NOT NULL,
  `attachment` text NOT NULL,
  `comment` text NOT NULL,
  `billable` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `followup`
--

DROP TABLE IF EXISTS `followup`;
CREATE TABLE `followup` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `followup_for` text NOT NULL,
  `type` text NOT NULL,
  `date` datetime NOT NULL,
  `comments` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reminder`
--

DROP TABLE IF EXISTS `reminder`;
CREATE TABLE `reminder` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `remind` text NOT NULL,
  `current_case_stage` text NOT NULL,
  `closed_by` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `user_type` int(11) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `document`
--
ALTER TABLE `document`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `followup`
--
ALTER TABLE `followup`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reminder`
--
ALTER TABLE `reminder`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `document`
--
ALTER TABLE `document`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `followup`
--
ALTER TABLE `followup`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reminder`
--
ALTER TABLE `reminder`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
