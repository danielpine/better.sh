/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 80019
Source Host           : localhost:3306
Source Database       : better

Target Server Type    : MYSQL
Target Server Version : 80019
File Encoding         : 65001

Date: 2022-04-13 18:18:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `search`
-- ----------------------------
DROP TABLE IF EXISTS `search`;
CREATE TABLE `search` (
  `id` int NOT NULL AUTO_INCREMENT,
  `search` varchar(255) DEFAULT NULL,
  `stime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of search
-- ----------------------------
INSERT INTO `search` VALUES ('1', '/record/list?state=%E7%99%BD%E6%9D%A8&current=1&pageSize=15&date=0328', '2022-04-13 18:10:28', null);
INSERT INTO `search` VALUES ('2', '/record/list?state=白杨小区&current=1&pageSize=15&date=0328', '2022-04-13 18:14:07', null);
INSERT INTO `search` VALUES ('3', '/record/list?state=白杨小区2&current=1&pageSize=15&date=0328', '2022-04-13 18:15:44', null);
INSERT INTO `search` VALUES ('4', '/record/list?state=白杨小&current=1&pageSize=15&date=0328', '2022-04-13 18:17:55', '::1');

-- ----------------------------
-- Table structure for `stat`
-- ----------------------------
DROP TABLE IF EXISTS `stat`;
CREATE TABLE `stat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `home` int DEFAULT NULL,
  `api` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of stat
-- ----------------------------
INSERT INTO `stat` VALUES ('1', '1002', '2007');
