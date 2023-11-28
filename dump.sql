-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.11.6-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for myprojectdb
CREATE DATABASE IF NOT EXISTS `myprojectdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `myprojectdb`;

-- Dumping structure for table myprojectdb.apps_userprofile
CREATE TABLE IF NOT EXISTS `apps_userprofile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(15) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `address` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `apps_userprofile_user_id_affa1678_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.apps_userprofile: ~3 rows (approximately)
INSERT INTO `apps_userprofile` (`id`, `phone_number`, `gender`, `address`, `user_id`) VALUES
	(1, '9841147588', 'male', 'kalanki', 4),
	(2, '9863196938', 'female', 'ason', 8),
	(3, '9863196938', 'female', 'Ason', 9);

-- Dumping structure for table myprojectdb.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.auth_group: ~0 rows (approximately)

-- Dumping structure for table myprojectdb.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table myprojectdb.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.auth_permission: ~28 rows (approximately)
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
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add pet owner', 7, 'add_petowner'),
	(26, 'Can change pet owner', 7, 'change_petowner'),
	(27, 'Can delete pet owner', 7, 'delete_petowner'),
	(28, 'Can view pet owner', 7, 'view_petowner'),
	(29, 'Can add user profile', 8, 'add_userprofile'),
	(30, 'Can change user profile', 8, 'change_userprofile'),
	(31, 'Can delete user profile', 8, 'delete_userprofile'),
	(32, 'Can view user profile', 8, 'view_userprofile');

-- Dumping structure for table myprojectdb.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.auth_user: ~2 rows (approximately)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(4, 'pbkdf2_sha256$600000$PYfhq1RWAC5LsuscSIMYmT$9qqWZOnv4hT/dD3UfprOe2cud4sVprVBLSOLPtFB1UE=', '2023-11-19 00:06:06.011709', 0, 'manoj@gmail.com', 'manoj', 'karki', 'manoj@gmail.com', 0, 1, '2023-11-18 23:25:32.414672'),
	(8, 'pbkdf2_sha256$600000$2sgzsEus6JOKOmh7pAffVN$5YsMpZFuQ1uGAsi9CXHd88A1Uh+EJ1bTbaZiPmaBma0=', '2023-11-18 23:43:09.855604', 0, 'luj@gmail.com', 'lujana', 'bajracharya', 'luj@gmail.com', 0, 1, '2023-11-18 23:43:08.980250'),
	(9, 'pbkdf2_sha256$600000$GfMq3HTB6yZWQ6cXsVA8Vh$DAIlYQmNIdGMvv6PBhRa/ERJdYHSqv3qSCn6pXh6Gmc=', '2023-11-20 06:26:45.606374', 0, 'lujanabajra@gmail.com', 'lujana', 'bajracharya', 'lujanabajra@gmail.com', 0, 1, '2023-11-20 06:26:29.518140');

-- Dumping structure for table myprojectdb.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.auth_user_groups: ~0 rows (approximately)

-- Dumping structure for table myprojectdb.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping structure for table myprojectdb.booking_details
CREATE TABLE IF NOT EXISTS `booking_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `pet_name` varchar(50) DEFAULT NULL,
  `breed` varchar(50) DEFAULT NULL,
  `age` varchar(50) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `disease` varchar(50) DEFAULT NULL,
  `ongoing_medication` varchar(50) DEFAULT NULL,
  `purpose_of_visit` varchar(50) DEFAULT NULL,
  `symptom` varchar(50) DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `tole` varchar(50) DEFAULT NULL,
  `house_number` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.booking_details: ~4 rows (approximately)
INSERT INTO `booking_details` (`id`, `email`, `phone`, `address`, `pet_name`, `breed`, `age`, `color`, `gender`, `disease`, `ongoing_medication`, `purpose_of_visit`, `symptom`, `method`, `city`, `tole`, `house_number`, `date`, `time`) VALUES
	(2, 'lujanabajra@gmail.com', '9863196938', 'Ason', 'Nimisha', 'Pugg', '12', 'Brown', 'Female', 'No', 'No', 'Vaccination', ' No', 'Test', 'Ktm', '12', '57', '2023-10-10', '1212'),
	(3, 'lujanabajra@gmail.com', '9863196938', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test ', 'test', 'test', 'test', 'test', 'test', 'test'),
	(5, 'test@gmail.com', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11', 'test12 ', 'test13', 'test14', 'test6', 'test16', 'test17', 'tet18'),
	(6, 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'testq', 'test', 'test ', 'test', 'test', 'test', 'test', 'test', 'test');

-- Dumping structure for table myprojectdb.contact_details
CREATE TABLE IF NOT EXISTS `contact_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `notes` longtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.contact_details: ~2 rows (approximately)
INSERT INTO `contact_details` (`id`, `first_name`, `last_name`, `email`, `phone`, `notes`) VALUES
	(1, 'test', 'test2', 'test@gmail.com', 'testing123', 'testing123asdasd'),
	(2, 'manoj', 'karki', 'manoj@gmail.com', 'testing123', 'tesadsdasjkdnasdjka'),
	(3, 'manoj', 'manoj', 'manoj@gmail.com', 'askdnasjkdn', 'qnasjkdnajkdnasd');

-- Dumping structure for table myprojectdb.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.django_admin_log: ~0 rows (approximately)

-- Dumping structure for table myprojectdb.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.django_content_type: ~8 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(7, 'apps', 'petowner'),
	(8, 'apps', 'userprofile'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session');

-- Dumping structure for table myprojectdb.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.django_migrations: ~18 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2023-11-08 06:43:53.101608'),
	(2, 'auth', '0001_initial', '2023-11-08 06:43:53.521776'),
	(3, 'admin', '0001_initial', '2023-11-08 06:43:53.587636'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2023-11-08 06:43:53.592622'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-08 06:43:53.598606'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2023-11-08 06:43:53.644484'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2023-11-08 06:43:53.674406'),
	(8, 'auth', '0003_alter_user_email_max_length', '2023-11-08 06:43:53.695350'),
	(9, 'auth', '0004_alter_user_username_opts', '2023-11-08 06:43:53.710310'),
	(10, 'auth', '0005_alter_user_last_login_null', '2023-11-08 06:43:53.737238'),
	(11, 'auth', '0006_require_contenttypes_0002', '2023-11-08 06:43:53.739234'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2023-11-08 06:43:53.745217'),
	(13, 'auth', '0008_alter_user_username_max_length', '2023-11-08 06:43:53.763674'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2023-11-08 06:43:53.783621'),
	(15, 'auth', '0010_alter_group_name_max_length', '2023-11-08 06:43:53.802570'),
	(16, 'auth', '0011_update_proxy_permissions', '2023-11-08 06:43:53.808555'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2023-11-08 06:43:53.829498'),
	(18, 'sessions', '0001_initial', '2023-11-08 06:43:53.860416'),
	(19, 'apps', '0001_initial', '2023-11-18 23:07:37.064322'),
	(20, 'apps', '0002_userprofile', '2023-11-18 23:22:47.130294'),
	(21, 'apps', '0003_delete_petowner', '2023-11-19 00:05:11.789660');

-- Dumping structure for table myprojectdb.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.django_session: ~3 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('0cdcowbzc8jdfyz8hylly92rt33cfj82', '.eJxVjDEOwjAMRe-SGUVJUR2HkZ0zRHbtkAJKpaadKu4OlTrA-t97fzOJ1qWktemcRjEXE83pd2Manlp3IA-q98kOU13mke2u2IM2e5tEX9fD_Tso1Mq3DizsfN-JJwfKoJQRmQIBnkm7DMgSMXrEkMURh4zgSHuCHLyAmvcHCKc42A:1r4xk5:Gve-X2FIcPaKJvYUA-bqa_ten_EsFZ3-1M0bfDyLhYQ', '2023-12-04 06:26:45.607681'),
	('ahy11rld1il0czk1fbvhjx5lnimihhzz', '.eJxVjDsOwjAQRO_iGlnr4C8lfc5g7XoNDiBHipMKcXccKQVMOe_NvEXEbS1xa3mJE4uL0OL02xGmZ6474AfW-yzTXNdlIrkr8qBNjjPn1_Vw_w4KttLXwSMPgAMYT9ZARkZlTdAaUg8kImSTVHaBwtk7ds4q1DfQ5LvLVny-7944hg:1r4VKA:wWxiaspD0eLbU109Dv_hQQJvvijHFGRkCp5Ewfr8GfQ', '2023-12-03 00:06:06.013705'),
	('xa114gb5r6gikgcadkbp0234863hgrw8', 'e30:1r4Ugv:HuyCM8F2qvRRbZEWT8axVexguJ8KE0QEMmH5C2fUkds', '2023-12-02 23:25:33.321869');

-- Dumping structure for table myprojectdb.pet_owner
CREATE TABLE IF NOT EXISTS `pet_owner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table myprojectdb.pet_owner: ~3 rows (approximately)
INSERT INTO `pet_owner` (`id`, `first_name`, `last_name`, `email`, `phone_number`, `gender`, `address`) VALUES
	(1, 'Manoj', 'Karki', 'manojgamer99@gmail.com', '+977 1234567890', 'male', 'kalanki'),
	(3, 'lujana', 'bajracharya', 'luj@gmail.com', '9863196938', 'female', 'ason'),
	(4, 'lujana', 'bajracharya', 'lujanabajra@gmail.com', '9863196938', 'female', 'Ason');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
