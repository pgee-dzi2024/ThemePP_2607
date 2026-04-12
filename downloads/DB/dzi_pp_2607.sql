-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Време на генериране: 12 апр 2026 в 15:44
-- Версия на сървъра: 10.4.32-MariaDB
-- Версия на PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данни: `dzi_pp_2607`
--

-- --------------------------------------------------------

--
-- Структура на таблица `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `auth_permission`
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
(25, 'Can add analysis', 7, 'add_analysis'),
(26, 'Can change analysis', 7, 'change_analysis'),
(27, 'Can delete analysis', 7, 'delete_analysis'),
(28, 'Can view analysis', 7, 'view_analysis');

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$wa69HjK5kgC4b6c8omaGHs$cFMDie+9dPx9Zzimr9sZcn8MPjuBs0S36p3XrbIwdNQ=', '2026-04-12 12:29:33.975786', 1, 'user_26', '', '', '', 1, 1, '2026-02-10 00:57:22.892428');

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'main', 'analysis'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Структура на таблица `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-02-10 00:56:43.526739'),
(2, 'auth', '0001_initial', '2026-02-10 00:56:43.981505'),
(3, 'admin', '0001_initial', '2026-02-10 00:56:44.117393'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-02-10 00:56:44.125420'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-02-10 00:56:44.132968'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-02-10 00:56:44.184661'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-02-10 00:56:44.236732'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-02-10 00:56:44.246941'),
(9, 'auth', '0004_alter_user_username_opts', '2026-02-10 00:56:44.254454'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-02-10 00:56:44.294146'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-02-10 00:56:44.296115'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-02-10 00:56:44.303142'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-02-10 00:56:44.314691'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-02-10 00:56:44.325926'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-02-10 00:56:44.338455'),
(16, 'auth', '0011_update_proxy_permissions', '2026-02-10 00:56:44.345887'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-02-10 00:56:44.356375'),
(18, 'sessions', '0001_initial', '2026-02-10 00:56:44.384878'),
(19, 'main', '0001_initial', '2026-04-11 23:50:47.613720');

-- --------------------------------------------------------

--
-- Структура на таблица `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('q0uuo2sf2s4qghnhlt9jniy5t6rhc5fe', '.eJxVjMEKwyAQRP_FcxHNumJ67L3fIKurNW0xEJNT6L83Qg7taWDem9mFp20tfmtp8ROLq9Di8tsFiq9UO-An1ccs41zXZQqyK_KkTd5nTu_b6f4dFGrlWEftbGY1Eg8GEhplGE3KwNrkbCFYBmTSw6gihODQaYLYsT6CEMXnC-k3OB0:1wBtpO:_fgQkdTOQVoA-gPkxxNh5V0lgTdutwbz60sMaGsCL0A', '2026-04-26 12:22:14.595079'),
('s2tumyw0ve9eoqrp39qcqi3noy6ngj80', '.eJydUMtOxDAM_JeeUZVnH3tEe-Gw0h44oUiREzu00JeaFK2E-HdSdpFA3DhZ9oxnxn4vLGyps1uk1fZYHApe3P2cOfCvNO0AvsD0PJd-ntLau3KnlDc0lqcZabi_cX8JdBC7vO15UwVkLaBQkrRiCrWiIJGrECrpKpQagYuWeelcoxsO0u8wzwW0zqLbMsyAhDb0A9kF0q57PBhzfHqwgonKmPPZmMeORrKstid47jOYRyNhD8ZcBaIxdbZG3mrwKJXw4HTg2ZY1lcDacVdehnj54zjBSPsl87hsidZoE8VkM_WbPkDu6bLMa7I-vv0n4nU7R_z6HbdN0FrUIihFXOWsrq65bpQCEVpWYVtmn-LjE5M7l5E:1wBuvs:OGvxYTgfcEhDiGbbWQdv9gRQsu7szWr0q1GqR3bZUIU', '2026-04-26 13:33:00.405393');

-- --------------------------------------------------------

--
-- Структура на таблица `main_analysis`
--

CREATE TABLE `main_analysis` (
  `id` bigint(20) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `total` double NOT NULL,
  `average` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_analysis`
--

INSERT INTO `main_analysis` (`id`, `filename`, `total`, `average`, `created_at`, `user_id`) VALUES
(1, 'products_csv.csv', 610, 122, '2026-04-12 09:54:56.748683', 1),
(2, 'products_csv.csv', 610, 122, '2026-04-12 09:56:08.432400', 1),
(3, 'dates_data_csv.csv', 3355, 167.75, '2026-04-12 09:56:16.845688', 1),
(4, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 09:57:32.972622', 1),
(5, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 09:57:46.743346', 1),
(6, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 10:13:58.740022', 1),
(7, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 10:46:06.690345', 1),
(8, 'expenses_data_xls.xlsx', 5300, 1060, '2026-04-12 10:50:00.924847', 1),
(9, 'students_data_xls.xlsx', 26, 5.2, '2026-04-12 10:50:23.819950', 1),
(10, 'laptops_test_xls.xlsx', 670, 111.67, '2026-04-12 10:50:39.349122', 1),
(11, 'monthly_sales_csv.csv', 3050, 254.17, '2026-04-12 10:51:11.712576', 1),
(12, 'monthly_sales_csv.csv', 3050, 254.17, '2026-04-12 11:10:46.437232', 1),
(13, 'monthly_sales_csv.csv', 3050, 3050, '2026-04-12 11:11:26.108747', 1),
(14, 'monthly_sales_csv.csv', 3050, 254.17, '2026-04-12 11:15:16.875708', 1),
(15, 'monthly_sales_csv.csv', 3050, 254.17, '2026-04-12 11:21:28.779087', 1),
(16, 'sales_data_xls.xlsx', 3810, 635, '2026-04-12 11:21:47.924584', 1),
(17, 'sales_data_xls.xlsx', 3810, 635, '2026-04-12 11:22:26.676114', 1),
(18, 'sales_data_xls.xlsx', 3810, 635, '2026-04-12 11:22:41.703416', 1),
(19, 'sales_data_xls.xlsx', 3810, 635, '2026-04-12 11:22:57.883302', 1),
(20, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 11:27:09.812877', 1),
(21, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 11:27:39.128987', 1),
(22, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 11:27:59.210455', 1),
(23, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 11:34:40.675879', 1),
(24, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 11:38:23.574104', 1),
(25, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 11:38:32.870341', 1),
(26, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 12:16:57.474772', 1),
(27, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 12:19:12.062194', 1),
(28, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 12:19:54.565641', 1),
(29, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 12:22:09.430274', 1),
(30, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 13:27:52.902781', 1),
(31, 'computers_test_xls.xlsx', 720, 120, '2026-04-12 13:33:00.394882', 1);

--
-- Indexes for dumped tables
--

--
-- Индекси за таблица `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индекси за таблица `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Индекси за таблица `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Индекси за таблица `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Индекси за таблица `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Индекси за таблица `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Индекси за таблица `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Индекси за таблица `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Индекси за таблица `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Индекси за таблица `main_analysis`
--
ALTER TABLE `main_analysis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_analysis_user_id_cff8ced5_fk_auth_user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `main_analysis`
--
ALTER TABLE `main_analysis`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Ограничения за дъмпнати таблици
--

--
-- Ограничения за таблица `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ограничения за таблица `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ограничения за таблица `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `main_analysis`
--
ALTER TABLE `main_analysis`
  ADD CONSTRAINT `main_analysis_user_id_cff8ced5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
