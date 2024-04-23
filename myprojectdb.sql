-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 24, 2024 at 08:01 AM
-- Server version: 10.11.4-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `myprojectdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_doctor`
--

CREATE TABLE `accounts_doctor` (
  `id` bigint(20) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `qualification` longtext DEFAULT NULL,
  `service_type` varchar(255) DEFAULT NULL,
  `nmc_number` varchar(255) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_doctor`
--

INSERT INTO `accounts_doctor` (`id`, `gender`, `mobile`, `address`, `qualification`, `service_type`, `nmc_number`, `image`, `status`, `created_on`, `updated_on`, `user_id`) VALUES
(4, 'Male', '9849227076', 'Budanilkantha', 'VMD', 'Laser Therapy', '456', 'doctor/Veterinary_Medical_Doctor_VMD__9xJrvtW.png', 1, '2024-02-18 12:08:09.574917', '2024-02-18 12:11:45.561119', 12),
(5, 'Female', '9849372054', 'Naxal', 'Vet Medicine Technician(VMT)', 'Orthopedic', '787', 'doctor/Registered_Veterinary_Nurse_RVN__Qv883N1.png', 1, '2024-02-19 17:17:53.504230', '2024-02-19 17:20:46.335600', 19);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_operator`
--

CREATE TABLE `accounts_operator` (
  `id` bigint(20) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_operator`
--

INSERT INTO `accounts_operator` (`id`, `gender`, `mobile`, `address`, `user_id`) VALUES
(3, 'Female', '9808229909', 'Baneshwor', 15);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_petowner`
--

CREATE TABLE `accounts_petowner` (
  `id` bigint(20) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_petowner`
--

INSERT INTO `accounts_petowner` (`id`, `gender`, `mobile`, `address`, `user_id`) VALUES
(5, 'Male', '9808588447', 'Baneshwor', 14);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user`
--

CREATE TABLE `accounts_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_operator` tinyint(1) NOT NULL,
  `is_patient` tinyint(1) NOT NULL,
  `is_doctor` tinyint(1) NOT NULL,
  `otp` varchar(255) DEFAULT NULL,
  `otp_created_at` datetime(6) NOT NULL,
  `otp_verified` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_user`
--

INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `is_admin`, `is_operator`, `is_patient`, `is_doctor`, `otp`, `otp_created_at`, `otp_verified`) VALUES
(1, 'pbkdf2_sha256$600000$ZizAStD2p1kDsgOSgE9DHu$5t82+CTdib4vc1JGa5iADbv4FTBsFygv04AHahy3TH8=', '2024-02-22 05:00:09.034349', 1, 'admin@admin.com', '', '', 'admin@admin.com', 1, 1, '2024-01-02 16:13:53.000000', 1, 0, 0, 0, NULL, '2024-01-02 16:13:53.559721', 0),
(12, 'pbkdf2_sha256$600000$BQDzSgKOEC6N4jM8o7Iz4e$fb6iUgKQH7SIVwqxNfzl+QfzuwQ2hbMILzcFlb35O9M=', '2024-02-22 01:06:30.401355', 0, 'produceandreap@gmail.com', 'Aatiz', 'Ghimire', 'produceandreap@gmail.com', 0, 1, '2024-02-18 12:08:09.309013', 0, 0, 0, 1, NULL, '2024-02-18 12:08:09.568914', 0),
(14, 'pbkdf2_sha256$600000$sZ1CSfnPrT3N8FeM0RiGhv$PXEvB8YmeFVq59MhryQgebXqzj0GQuY8ULY68L8e2Bk=', '2024-02-22 05:37:28.509472', 0, '9808588447raju@gmail.com', 'Pet', 'Owner', '9808588447raju@gmail.com', 0, 1, '2024-02-18 12:16:38.744348', 0, 0, 1, 0, NULL, '2024-02-18 12:16:39.036567', 0),
(15, 'pbkdf2_sha256$600000$DJX77ENyr5k7CP2Giy6FKy$Sp1V6xMDgX+26ytg1N4vvhc3MnJlOCTSsG4dTrMCCUc=', '2024-02-22 01:02:51.037351', 0, '9808229909nila@gmail.com', 'Nilaa', 'Pradha', '9808229909nila@gmail.com', 0, 1, '2024-02-19 16:49:22.308371', 0, 1, 0, 0, NULL, '2024-02-19 16:49:22.801512', 0),
(19, 'pbkdf2_sha256$600000$qtn2Uulpz1XLjnfnNFeoFz$r/Jzfyci/bWVVS+NtQ5Ocv7mbuETM3eGmGqR1NO1hP4=', '2024-02-22 01:05:31.989627', 0, 'pradhannitesh10@gmail.com', 'Nimisha', 'Pradhann', 'pradhannitesh10@gmail.com', 0, 1, '2024-02-19 17:17:52.968564', 0, 0, 0, 1, NULL, '2024-02-19 17:17:53.494889', 0);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_groups`
--

CREATE TABLE `accounts_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_user_permissions`
--

CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `account_emailaddress`
--

CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `account_emailconfirmation`
--

CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add pet owner', 7, 'add_petowner'),
(26, 'Can change pet owner', 7, 'change_petowner'),
(27, 'Can delete pet owner', 7, 'delete_petowner'),
(28, 'Can view pet owner', 7, 'view_petowner'),
(29, 'Can add operator', 8, 'add_operator'),
(30, 'Can change operator', 8, 'change_operator'),
(31, 'Can delete operator', 8, 'delete_operator'),
(32, 'Can view operator', 8, 'view_operator'),
(33, 'Can add doctor', 9, 'add_doctor'),
(34, 'Can change doctor', 9, 'change_doctor'),
(35, 'Can delete doctor', 9, 'delete_doctor'),
(36, 'Can view doctor', 9, 'view_doctor'),
(37, 'Can add contact', 10, 'add_contact'),
(38, 'Can change contact', 10, 'change_contact'),
(39, 'Can delete contact', 10, 'delete_contact'),
(40, 'Can view contact', 10, 'view_contact'),
(41, 'Can add feedback', 11, 'add_feedback'),
(42, 'Can change feedback', 11, 'change_feedback'),
(43, 'Can delete feedback', 11, 'delete_feedback'),
(44, 'Can view feedback', 11, 'view_feedback'),
(45, 'Can add booking', 12, 'add_booking'),
(46, 'Can change booking', 12, 'change_booking'),
(47, 'Can delete booking', 12, 'delete_booking'),
(48, 'Can view booking', 12, 'view_booking'),
(49, 'Can add service', 13, 'add_service'),
(50, 'Can change service', 13, 'change_service'),
(51, 'Can delete service', 13, 'delete_service'),
(52, 'Can view service', 13, 'view_service'),
(53, 'Can add time', 14, 'add_time'),
(54, 'Can change time', 14, 'change_time'),
(55, 'Can delete time', 14, 'delete_time'),
(56, 'Can view time', 14, 'view_time'),
(57, 'Can add payment', 15, 'add_payment'),
(58, 'Can change payment', 15, 'change_payment'),
(59, 'Can delete payment', 15, 'delete_payment'),
(60, 'Can view payment', 15, 'view_payment'),
(61, 'Can add association', 16, 'add_association'),
(62, 'Can change association', 16, 'change_association'),
(63, 'Can delete association', 16, 'delete_association'),
(64, 'Can view association', 16, 'view_association'),
(65, 'Can add code', 17, 'add_code'),
(66, 'Can change code', 17, 'change_code'),
(67, 'Can delete code', 17, 'delete_code'),
(68, 'Can view code', 17, 'view_code'),
(69, 'Can add nonce', 18, 'add_nonce'),
(70, 'Can change nonce', 18, 'change_nonce'),
(71, 'Can delete nonce', 18, 'delete_nonce'),
(72, 'Can view nonce', 18, 'view_nonce'),
(73, 'Can add user social auth', 19, 'add_usersocialauth'),
(74, 'Can change user social auth', 19, 'change_usersocialauth'),
(75, 'Can delete user social auth', 19, 'delete_usersocialauth'),
(76, 'Can view user social auth', 19, 'view_usersocialauth'),
(77, 'Can add partial', 20, 'add_partial'),
(78, 'Can change partial', 20, 'change_partial'),
(79, 'Can delete partial', 20, 'delete_partial'),
(80, 'Can view partial', 20, 'view_partial'),
(81, 'Can add email address', 21, 'add_emailaddress'),
(82, 'Can change email address', 21, 'change_emailaddress'),
(83, 'Can delete email address', 21, 'delete_emailaddress'),
(84, 'Can view email address', 21, 'view_emailaddress'),
(85, 'Can add email confirmation', 22, 'add_emailconfirmation'),
(86, 'Can change email confirmation', 22, 'change_emailconfirmation'),
(87, 'Can delete email confirmation', 22, 'delete_emailconfirmation'),
(88, 'Can view email confirmation', 22, 'view_emailconfirmation'),
(89, 'Can add social account', 23, 'add_socialaccount'),
(90, 'Can change social account', 23, 'change_socialaccount'),
(91, 'Can delete social account', 23, 'delete_socialaccount'),
(92, 'Can view social account', 23, 'view_socialaccount'),
(93, 'Can add social application', 24, 'add_socialapp'),
(94, 'Can change social application', 24, 'change_socialapp'),
(95, 'Can delete social application', 24, 'delete_socialapp'),
(96, 'Can view social application', 24, 'view_socialapp'),
(97, 'Can add social application token', 25, 'add_socialtoken'),
(98, 'Can change social application token', 25, 'change_socialtoken'),
(99, 'Can delete social application token', 25, 'delete_socialtoken'),
(100, 'Can view social application token', 25, 'view_socialtoken');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-01-02 16:14:42.749089', '1', 'admin@admin.com', 2, '[{\"changed\": {\"fields\": [\"Username\", \"Is admin\"]}}]', 6, 1),
(2, '2024-01-03 07:51:06.558046', '1', 'bigyandhakal377', 3, '', 19, 1),
(3, '2024-01-03 07:58:24.149019', '2', 'bigyandhakal3779d0ff4b2415a4dc3', 3, '', 19, 1),
(4, '2024-01-03 08:12:21.917015', '3', 'bigyandhakal3779d0ff4b2415a4dc3', 3, '', 6, 1),
(5, '2024-01-03 08:12:21.936469', '2', 'bigyandhakal377', 3, '', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(21, 'account', 'emailaddress'),
(22, 'account', 'emailconfirmation'),
(9, 'accounts', 'doctor'),
(8, 'accounts', 'operator'),
(7, 'accounts', 'petowner'),
(6, 'accounts', 'user'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(10, 'information', 'contact'),
(11, 'information', 'feedback'),
(12, 'service', 'booking'),
(15, 'service', 'payment'),
(13, 'service', 'service'),
(14, 'service', 'time'),
(5, 'sessions', 'session'),
(23, 'socialaccount', 'socialaccount'),
(24, 'socialaccount', 'socialapp'),
(25, 'socialaccount', 'socialtoken'),
(16, 'social_django', 'association'),
(17, 'social_django', 'code'),
(18, 'social_django', 'nonce'),
(20, 'social_django', 'partial'),
(19, 'social_django', 'usersocialauth');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-01-02 16:13:26.293717'),
(2, 'contenttypes', '0002_remove_content_type_name', '2024-01-02 16:13:26.364715'),
(3, 'auth', '0001_initial', '2024-01-02 16:13:26.571716'),
(4, 'auth', '0002_alter_permission_name_max_length', '2024-01-02 16:13:26.635716'),
(5, 'auth', '0003_alter_user_email_max_length', '2024-01-02 16:13:26.646717'),
(6, 'auth', '0004_alter_user_username_opts', '2024-01-02 16:13:26.653713'),
(7, 'auth', '0005_alter_user_last_login_null', '2024-01-02 16:13:26.662717'),
(8, 'auth', '0006_require_contenttypes_0002', '2024-01-02 16:13:26.665718'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2024-01-02 16:13:26.673719'),
(10, 'auth', '0008_alter_user_username_max_length', '2024-01-02 16:13:26.682714'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2024-01-02 16:13:26.691730'),
(12, 'auth', '0010_alter_group_name_max_length', '2024-01-02 16:13:26.707723'),
(13, 'auth', '0011_update_proxy_permissions', '2024-01-02 16:13:26.716715'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2024-01-02 16:13:26.722715'),
(15, 'accounts', '0001_initial', '2024-01-02 16:13:27.277716'),
(16, 'admin', '0001_initial', '2024-01-02 16:13:27.403714'),
(17, 'admin', '0002_logentry_remove_auto_add', '2024-01-02 16:13:27.417714'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2024-01-02 16:13:27.434714'),
(19, 'information', '0001_initial', '2024-01-02 16:13:27.471719'),
(20, 'service', '0001_initial', '2024-01-02 16:13:27.846715'),
(21, 'sessions', '0001_initial', '2024-01-02 16:13:27.889716'),
(22, 'default', '0001_initial', '2024-01-03 07:48:37.874904'),
(23, 'social_auth', '0001_initial', '2024-01-03 07:48:37.884279'),
(24, 'default', '0002_add_related_name', '2024-01-03 07:48:37.907241'),
(25, 'social_auth', '0002_add_related_name', '2024-01-03 07:48:37.916243'),
(26, 'default', '0003_alter_email_max_length', '2024-01-03 07:48:37.943601'),
(27, 'social_auth', '0003_alter_email_max_length', '2024-01-03 07:48:37.966645'),
(28, 'default', '0004_auto_20160423_0400', '2024-01-03 07:48:37.992063'),
(29, 'social_auth', '0004_auto_20160423_0400', '2024-01-03 07:48:37.999062'),
(30, 'social_auth', '0005_auto_20160727_2333', '2024-01-03 07:48:38.028066'),
(31, 'social_django', '0006_partial', '2024-01-03 07:48:38.081149'),
(32, 'social_django', '0007_code_timestamp', '2024-01-03 07:48:38.118924'),
(33, 'social_django', '0008_partial_timestamp', '2024-01-03 07:48:38.156885'),
(34, 'social_django', '0009_auto_20191118_0520', '2024-01-03 07:48:38.209344'),
(35, 'social_django', '0010_uid_db_index', '2024-01-03 07:48:38.241502'),
(36, 'social_django', '0004_auto_20160423_0400', '2024-01-03 07:48:38.255077'),
(37, 'social_django', '0003_alter_email_max_length', '2024-01-03 07:48:38.261114'),
(38, 'social_django', '0005_auto_20160727_2333', '2024-01-03 07:48:38.265164'),
(39, 'social_django', '0002_add_related_name', '2024-01-03 07:48:38.276817'),
(40, 'social_django', '0001_initial', '2024-01-03 07:48:38.284177'),
(41, 'social_django', '0011_alter_id_fields', '2024-01-03 10:56:54.680949'),
(42, 'account', '0001_initial', '2024-02-18 11:54:13.801530'),
(43, 'account', '0002_email_max_length', '2024-02-18 11:54:13.826630'),
(44, 'account', '0003_alter_emailaddress_create_unique_verified_email', '2024-02-18 11:54:13.856422'),
(45, 'account', '0004_alter_emailaddress_drop_unique_email', '2024-02-18 11:54:14.634969'),
(46, 'account', '0005_emailaddress_idx_upper_email', '2024-02-18 11:54:14.645967'),
(47, 'socialaccount', '0001_initial', '2024-02-18 11:54:14.790317'),
(48, 'socialaccount', '0002_token_max_lengths', '2024-02-18 11:54:14.833802'),
(49, 'socialaccount', '0003_extra_data_default_dict', '2024-02-18 11:54:14.843704'),
(50, 'socialaccount', '0004_app_provider_id_settings', '2024-02-18 11:54:14.902156'),
(51, 'socialaccount', '0005_socialtoken_nullable_app', '2024-02-18 11:54:15.179934');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('9cmawfkyex2wyrz828yhdq3mhigrlmby', 'eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoiQzNsYzRBQXZ2eHFPVmRvMkx3RXpBZWhiWjVSNVVYaFcifQ:1rKvzm:BFRWh2JJ1frViM_jwHf1l3FXpd7jNZpIekLUrL0brlA', '2024-01-06 07:48:58.680684'),
('fj89c4tv8u9z4zkljh36v9giqul4dmy6', 'eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoibjQ2TnFZQU9rQjMwMFNVTDZydXFvVXJjVmhCV2JYTU0ifQ:1rKjWc:RLtap_c1VgtAUkwrgokoBWSCp_EdUXA6jQRTHZFWv1I', '2024-01-05 18:30:02.664544'),
('g15se9n1posctsjqiqy4hio22u2nhc16', '.eJxVkMsKwjAQRf8lay1pxjx0J4IuBEVU0FWYJumDFiNNRET8d1t1YVcDdzj3DPMkhfdF48Yeb7FkOkSMjsxIJdaH_LRY7lS7zo6T6V7F-X212e-uj3OsJzUZEd0T-hZcqyvbITDMMjS1u_SL4E2FjTa-dckvDclXm6w-Yzvv5UO-xFB2sEo5T9EwlIYxKVAhsJxTjiAkOGk5B8ogBcymAMJKSZ0FSlHlGRMWeVf683-qGwxRN76oLn8HDl5AXm9ARFu9:1rKw2y:QDGpvFqN-epPk7zVY8WO0UkTkKr91v0G1qomHqTzTbU', '2024-01-06 07:52:16.881089'),
('grjlixomueskzba1dbygbig37wxz3bdx', '.eJxVjEsOwiAYBu_C2hC0PIpL9z0D-X4eUjWQlHZlvLsl6UK3M5N5M4dtzW5rcXFzYFd2ZqdfRvDPWLoID5R75b6WdZmJ94QftvGphvi6He3fIKPlvk3SCqGlFNBGG8CaUSJQglFhkIYMFEarhl1QsMMFPtkU90gjKkvs8wXQkDfv:1rLOpw:9tC5L5x6ugD74f2CAc4OP__VKHUcwGg0Ub5rxP1G7XA', '2024-01-07 14:36:44.574613'),
('nb3l0emsynzxj8mdb2ndnqi7phxupyp4', 'eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoiRjh1UTM5eklWaHVPVWF1UjRxY2FkMFBBVkJqNzdlODIifQ:1rKjWA:qOb7aWrNKN6s8OAU3s5bRiMZOxVQIVyvGY2EQvgfTCE', '2024-01-05 18:29:34.422391'),
('s6fnpuyzwcdnhug9n04jpbhdajwet58s', '.eJxVjDkOwjAUBe_iGllesUNJzxmsv9g4gBwpTirE3UmkFNDOzHtvkWBdalp7ntPI4iK0OP0yBHrmtgt-QLtPkqa2zCPKPZGH7fI2cX5dj_bvoEKv2xoDFesAoTA6Y6weQGlbgiNg0P5sOBvyLgQspHjwUemNqaKzUTFaFp8v_p44FA:1rKhPB:dfssoLkSqzzZWg-Po36hXXRBFjwX4g1Bhe8cDBk43c0', '2024-01-05 16:14:13.534256'),
('vy863wtcquncaufvoeblul1kslokkjnx', 'eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoiajc2eHRMQ1dMS05mZVdQOGhobTRUQ0JZOUp1YUNLT0cifQ:1rKvlq:CeTnkSFinY8S2PnVrmoQ9G4jcvlKjYuLGEL5pRIXKIk', '2024-01-06 07:34:34.214314');

-- --------------------------------------------------------

--
-- Table structure for table `information_contact`
--

CREATE TABLE `information_contact` (
  `id` bigint(20) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `notes` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `information_contact`
--

INSERT INTO `information_contact` (`id`, `first_name`, `last_name`, `email`, `phone`, `notes`) VALUES
(4, 'Aarav', 'Pradhan', 'Aaravpradhan12365@gmail.com', '9803370278', 'My dog has got cherry eyes. Do you also treat eye problems?');

-- --------------------------------------------------------

--
-- Table structure for table `information_feedback`
--

CREATE TABLE `information_feedback` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `details` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `service_booking`
--

CREATE TABLE `service_booking` (
  `id` bigint(20) NOT NULL,
  `purchase_id` char(32) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `petname` varchar(255) DEFAULT NULL,
  `breed` varchar(255) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `name_of_Disease` varchar(255) DEFAULT NULL,
  `on_going_medication` varchar(255) DEFAULT NULL,
  `purpose_of_visit` varchar(255) DEFAULT NULL,
  `symptonm_of_Disease` varchar(255) DEFAULT NULL,
  `booking_type` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `tole` varchar(255) DEFAULT NULL,
  `houseNumber` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `booking_status` varchar(255) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `doctor_id` bigint(20) NOT NULL,
  `service_id` bigint(20) NOT NULL,
  `time_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_booking`
--

INSERT INTO `service_booking` (`id`, `purchase_id`, `email`, `phone`, `address`, `petname`, `breed`, `age`, `color`, `gender`, `name_of_Disease`, `on_going_medication`, `purpose_of_visit`, `symptonm_of_Disease`, `booking_type`, `city`, `tole`, `houseNumber`, `location`, `date`, `booking_status`, `status`, `created_on`, `updated_on`, `doctor_id`, `service_id`, `time_id`, `user_id`) VALUES
(14, 'a262b402468545a1935bc47d98fcb40c', '9808588447raju@gmail.com', '9808588447', 'Baneshwor', 'Atom', 'Husky', 4, 'Black', 'Female', 'Leg fracture', 'None', NULL, 'None', 'Clinic', '', '4', '', '', '2024-02-22', 'Confirmed', 1, '2024-02-19 17:33:47.838712', '2024-02-19 17:34:12.702184', 5, 3, 1, 14),
(15, '531a56e51f5f4040b2b1910e99ac7c78', '9808588447raju@gmail.com', '9808588447', 'Baneshwor', 'Hulk', 'German Shepherd', 1, 'Brown', 'Female', 'Ear Infections', 'Ketaconazole', NULL, 'Skin infections', 'Clinic', '', '1', '', '', '2024-02-22', 'Cancelled', 0, '2024-02-22 04:36:51.862908', '2024-02-22 04:38:12.490417', 5, 4, 2, 14),
(16, '87fbf6d62cc74e2e8ebec3791c50ddb2', '9808588447raju@gmail.com', '9808588447', 'Baneshwor', 'Tommy', 'Dalmation', 5, 'Brown', 'Male', 'Leg fracture', 'Ketaconazole', NULL, 'High Temperature', 'Clinic', '', '5', '', '', '2024-02-23', 'Requested', 0, '2024-02-22 05:39:40.639948', '2024-02-22 05:39:40.639948', 4, 3, 2, 14);

-- --------------------------------------------------------

--
-- Table structure for table `service_payment`
--

CREATE TABLE `service_payment` (
  `id` bigint(20) NOT NULL,
  `payment_id` varchar(255) DEFAULT NULL,
  `payment_method` varchar(255) NOT NULL,
  `payment_completed` tinyint(1) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `booking_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_payment`
--

INSERT INTO `service_payment` (`id`, `payment_id`, `payment_method`, `payment_completed`, `status`, `created_on`, `updated_on`, `booking_id`) VALUES
(5, '4kVW4u3vh458s4LcEFYvPE', 'Khalti', 1, 1, '2024-02-19 17:34:12.705581', '2024-02-19 17:34:12.707571', 14),
(6, 'CGoFJ8NuDCUgpTZt7WKDZV', 'Khalti', 1, 1, '2024-02-22 04:37:37.210192', '2024-02-22 04:37:37.212209', 15);

-- --------------------------------------------------------

--
-- Table structure for table `service_service`
--

CREATE TABLE `service_service` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `details` longtext DEFAULT NULL,
  `price` double DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `updated_on` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_service`
--

INSERT INTO `service_service` (`id`, `title`, `details`, `price`, `image`, `status`, `created_on`, `updated_on`) VALUES
(3, 'Pain Management', 'This is pain management.', 10, 'services/Pain_Management_HSK0bp4.png', 1, '2024-02-19 17:24:59.922978', '2024-02-19 17:24:59.922978'),
(4, 'Orthopedic Surgery', 'Orthopedic surgery is important', 10, 'services/Orthopedic_Surgery.png', 1, '2024-02-19 17:25:55.885321', '2024-02-19 17:25:55.885321'),
(5, 'Dental Checkup', 'This is dental', 10, 'services/Dental_Care_uL37TTX.png', 1, '2024-02-19 17:27:09.689906', '2024-02-19 17:27:09.689906');

-- --------------------------------------------------------

--
-- Table structure for table `service_time`
--

CREATE TABLE `service_time` (
  `id` bigint(20) NOT NULL,
  `start_time` time(6) DEFAULT NULL,
  `end_time` time(6) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `available_daytimes` longtext DEFAULT NULL,
  `occupied_daytimes` longtext DEFAULT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_time`
--

INSERT INTO `service_time` (`id`, `start_time`, `end_time`, `duration`, `available_daytimes`, `occupied_daytimes`, `status`) VALUES
(1, '09:00:00.000000', '10:00:00.000000', NULL, '', '', 1),
(2, '10:00:00.000000', '11:00:00.000000', NULL, '', '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialaccount`
--

CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp`
--

CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`settings`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialtoken`
--

CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_association`
--

CREATE TABLE `social_auth_association` (
  `id` bigint(20) NOT NULL,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_code`
--

CREATE TABLE `social_auth_code` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_nonce`
--

CREATE TABLE `social_auth_nonce` (
  `id` bigint(20) NOT NULL,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(65) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_partial`
--

CREATE TABLE `social_auth_partial` (
  `id` bigint(20) NOT NULL,
  `token` varchar(32) NOT NULL,
  `next_step` smallint(5) UNSIGNED NOT NULL CHECK (`next_step` >= 0),
  `backend` varchar(32) NOT NULL,
  `data` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_usersocialauth`
--

CREATE TABLE `social_auth_usersocialauth` (
  `id` bigint(20) NOT NULL,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts_doctor`
--
ALTER TABLE `accounts_doctor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `accounts_operator`
--
ALTER TABLE `accounts_operator`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `accounts_petowner`
--
ALTER TABLE `accounts_petowner`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `accounts_user`
--
ALTER TABLE `accounts_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  ADD KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  ADD KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`);

--
-- Indexes for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key` (`key`),
  ADD KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `information_contact`
--
ALTER TABLE `information_contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `information_feedback`
--
ALTER TABLE `information_feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `service_booking`
--
ALTER TABLE `service_booking`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `purchase_id` (`purchase_id`),
  ADD KEY `service_booking_service_id_952453c9_fk_service_service_id` (`service_id`),
  ADD KEY `service_booking_time_id_fc5db4f6_fk_service_time_id` (`time_id`),
  ADD KEY `service_booking_user_id_471c8c09_fk_accounts_user_id` (`user_id`),
  ADD KEY `service_booking_doctor_id_30c05d54_fk_accounts_doctor_id` (`doctor_id`);

--
-- Indexes for table `service_payment`
--
ALTER TABLE `service_payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_payment_booking_id_e40b7160_fk_service_booking_id` (`booking_id`);

--
-- Indexes for table `service_service`
--
ALTER TABLE `service_service`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `service_time`
--
ALTER TABLE `service_time`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  ADD KEY `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `socialaccount_socialapp`
--
ALTER TABLE `socialaccount_socialapp`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  ADD KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`);

--
-- Indexes for table `social_auth_association`
--
ALTER TABLE `social_auth_association`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`);

--
-- Indexes for table `social_auth_code`
--
ALTER TABLE `social_auth_code`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  ADD KEY `social_auth_code_code_a2393167` (`code`),
  ADD KEY `social_auth_code_timestamp_176b341f` (`timestamp`);

--
-- Indexes for table `social_auth_nonce`
--
ALTER TABLE `social_auth_nonce`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`);

--
-- Indexes for table `social_auth_partial`
--
ALTER TABLE `social_auth_partial`
  ADD PRIMARY KEY (`id`),
  ADD KEY `social_auth_partial_token_3017fea3` (`token`),
  ADD KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`);

--
-- Indexes for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  ADD KEY `social_auth_usersocialauth_user_id_17d28448_fk_accounts_user_id` (`user_id`),
  ADD KEY `social_auth_usersocialauth_uid_796e51dc` (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts_doctor`
--
ALTER TABLE `accounts_doctor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `accounts_operator`
--
ALTER TABLE `accounts_operator`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `accounts_petowner`
--
ALTER TABLE `accounts_petowner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `accounts_user`
--
ALTER TABLE `accounts_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `information_contact`
--
ALTER TABLE `information_contact`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `information_feedback`
--
ALTER TABLE `information_feedback`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `service_booking`
--
ALTER TABLE `service_booking`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `service_payment`
--
ALTER TABLE `service_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `service_service`
--
ALTER TABLE `service_service`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `service_time`
--
ALTER TABLE `service_time`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `socialaccount_socialapp`
--
ALTER TABLE `socialaccount_socialapp`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_association`
--
ALTER TABLE `social_auth_association`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_code`
--
ALTER TABLE `social_auth_code`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_nonce`
--
ALTER TABLE `social_auth_nonce`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_partial`
--
ALTER TABLE `social_auth_partial`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_doctor`
--
ALTER TABLE `accounts_doctor`
  ADD CONSTRAINT `accounts_doctor_user_id_d06b185a_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_operator`
--
ALTER TABLE `accounts_operator`
  ADD CONSTRAINT `accounts_operator_user_id_fa7a2dae_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_petowner`
--
ALTER TABLE `accounts_petowner`
  ADD CONSTRAINT `accounts_petowner_user_id_33bc1d29_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  ADD CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  ADD CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  ADD CONSTRAINT `account_emailaddress_user_id_2c513194_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  ADD CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `service_booking`
--
ALTER TABLE `service_booking`
  ADD CONSTRAINT `service_booking_doctor_id_30c05d54_fk_accounts_doctor_id` FOREIGN KEY (`doctor_id`) REFERENCES `accounts_doctor` (`id`),
  ADD CONSTRAINT `service_booking_service_id_952453c9_fk_service_service_id` FOREIGN KEY (`service_id`) REFERENCES `service_service` (`id`),
  ADD CONSTRAINT `service_booking_time_id_fc5db4f6_fk_service_time_id` FOREIGN KEY (`time_id`) REFERENCES `service_time` (`id`),
  ADD CONSTRAINT `service_booking_user_id_471c8c09_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `service_payment`
--
ALTER TABLE `service_payment`
  ADD CONSTRAINT `service_payment_booking_id_e40b7160_fk_service_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `service_booking` (`id`);

--
-- Constraints for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  ADD CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  ADD CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  ADD CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`);

--
-- Constraints for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  ADD CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
