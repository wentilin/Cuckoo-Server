drop database if exists cuckoodb;

create database cuckoodb;

use cuckoodb;

grant select, insert, update, delete on cuckoodb.* to 'www-data'@'localhost' identified by 'www-data';

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '昵称',
  `phone` varchar(32) CHARACTER SET utf8mb4 NOT NULL COMMENT '手机',
  `avatarUrl` varchar(128) CHARACTER SET utf8mb4 NOT NULL COMMENT '头像',
  `avatarUrlOrigin` varchar(128) CHARACTER SET utf8mb4 DEFAULT NULL,
  `gender` tinyint(4) DEFAULT '0' COMMENT '性别，0是男，1是女',
  `passwd` varchar(128) CHARACTER SET utf8mb4 NOT NULL COMMENT '密码',
  `salt` varchar(64) CHARACTER SET utf8mb4 NOT NULL COMMENT '盐值',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态，1有效，0删除',
  `cts` real DEFAULT NULL,
  `uts` real DEFAULT NULL,
  `area` varchar(64) DEFAULT NULL COMMENT '所在地区',
  `coverUrl` varchar(128) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '个人封面大图',
  `signature` varchar(128) DEFAULT NULL COMMENT '个性签名',
  `followCount` int(11) DEFAULT '0' COMMENT '关注者人数',
  `followedCount` int(11) DEFAULT '0' COMMENT '被关注人数',
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_UNIQUE` (`phone`,`status`),
  UNIQUE KEY `name_UNIQUE` (`name`,`status`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `user_follow` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `followUid` bigint(20) DEFAULT NULL COMMENT '关注对象uid',
  `cts` real DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_unique` (`uid`,`followUid`),
  KEY `idx_uid` (`uid`),
  KEY `idx_follow` (`followUid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `user_session` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `sessionId` varchar(128) NOT NULL,
  `cts` real DEFAULT NULL,
  `uts` real DEFAULT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '1',
  `device` tinyint(4) NOT NULL DEFAULT '0' COMMENT '设备，0代表web，1表示移动端。默认是web',
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id_UNIQUE` (`sessionId`,`status`,`device`),
  KEY `uid_idx` (`uid`,`device`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET= utf8mb4;

CREATE TABLE `feed` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `coverImg` varchar(128) CHARACTER SET utf8mb4 DEFAULT NULL,
  `desc` varchar(256) DEFAULT NULL,
  `content` text,
  `cts` real DEFAULT NULL,
  `uts` real DEFAULT NULL,
  `status` tinyint(4) DEFAULT '1' COMMENT '1表示有效，0表示删除',
  `shareCode` varchar(64) CHARACTER SET utf8mb4 DEFAULT NULL,
  `likeCount` int(11) DEFAULT '0',
  `commentCount` int(11) DEFAULT '0'
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`,`cts`),
  KEY `idx_share` (`shareCode`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `feed_timeline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `fid` bigint(20) DEFAULT NULL,
  `authorId` bigint(20) DEFAULT NULL,
  `cts` real DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`,`cts`),
  KEY `idx_fid` (`fid`),
  KEY `idx_aid` (`uid`,`authorId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `feed_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fid` bigint(20) DEFAULT NULL,
  `content` text,
  `uid` bigint(20) DEFAULT NULL,
  `uname` varchar(64) NOT NULL COMMENT '昵称',
  `avatarUrl` varchar(128) CHARACTER SET utf8mb4 NOT NULL COMMENT '头像',
  `cts` real DEFAULT NULL,
  `status` tinyint(4) DEFAULT '1' COMMENT '1表示有效，0表示删除',
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`,`cts`),
  KEY `idx_fid` (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `feed_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fid` bigint(20) DEFAULT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `uname` varchar(64) NOT NULL COMMENT '昵称',
  `avatarUrl` varchar(128) CHARACTER SET utf8mb4 NOT NULL COMMENT '头像',
  `toUid` bigint(20) DEFAULT 0,
  `toUname` varchar(64) DEFAULT NULL,
  `cts` real DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vote_id_UNIQUE` (`fid`,`uid`),
  KEY `idx_uid` (`uid`,`cts`),
  KEY `idx_fid` (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

