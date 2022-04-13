/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 80019
Source Host           : localhost:3306
Source Database       : better

Target Server Type    : MYSQL
Target Server Version : 80019
File Encoding         : 65001

Date: 2022-04-13 09:22:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `urls`
-- ----------------------------
DROP TABLE IF EXISTS `urls`;
CREATE TABLE `urls` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of urls
-- ----------------------------
