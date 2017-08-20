use cuckoodb;
CREATE TABLE IF NOT EXISTS `feed_comment` (
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


CREATE TABLE IF NOT EXISTS `feed_vote` (
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

-- CALL Pro_ColumnWork ('BaseInfo','Name2',4,'VARCHAR(50)');
DROP PROCEDURE IF EXISTS Pro_ColumnWork;
DELIMITER $$
-- 1表示新增列,2表示修改列类型，3表示修改列名称，4表示删除列
CREATE PROCEDURE Pro_ColumnWork(TableName VARCHAR(50),ColumnName VARCHAR(50),CType INT,SqlStr VARCHAR(4000))
BEGIN
	DECLARE Rows1 INT;
	SET Rows1=0;
	SELECT COUNT(*) INTO Rows1  FROM INFORMATION_SCHEMA.Columns
	WHERE table_schema= DATABASE() AND table_name=TableName AND column_name=ColumnName;
	-- 新增列
	IF (CType=1 AND Rows1<=0) THEN
		SET SqlStr := CONCAT( 'ALTER TABLE `',TableName,'` ADD COLUMN `',ColumnName,'` ',SqlStr);
	-- 修改列类型
	ELSEIF (CType=2 AND Rows1>0)  THEN
		SET SqlStr := CONCAT('ALTER TABLE `',TableName,'` MODIFY `',ColumnName,'` ',SqlStr);
	-- 修改列名称
	ELSEIF (CType=3 AND Rows1>0) THEN
		SET SqlStr := CONCAT('ALTER TABLE `',TableName,'` CHANGE `',ColumnName,'` ',SqlStr);
	-- 删除列
	ELSEIF (CType=4 AND Rows1>0) THEN
		SET SqlStr := CONCAT('ALTER TABLE `',TableName,'` DROP COLUMN `',ColumnName, '`');
	ELSE
		SET SqlStr := '';
	END IF;
	-- 执行命令
	IF (SqlStr<>'') THEN
		SET @SQL1 = SqlStr;
		PREPARE stmt1 FROM @SQL1;
		EXECUTE stmt1;
	END IF;
END
$$
DELIMITER ;

-- 修改`feed`表字段`like`为`likeCount`
CALL Pro_ColumnWork ('feed','like', 3, '`likeCount` int(11)');
-- `feed`表增加字段`commentCount`
CALL Pro_ColumnWork ('feed','commentCount', 1, 'int(11) DEFAULT 0');
-- `feed_comment`表增加字段`status`
CALL Pro_ColumnWork('feed_comment', 'status', 1, 'tinyint(4) DEFAULT 1');
-- `feed_comment`表增加字段`toUid`
CALL Pro_ColumnWork('feed_comment', 'toUid', 1, 'bigint(20) DEFAULT 0');
-- `feed_comment`表增加字段`toUname`
CALL Pro_ColumnWork('feed_comment', 'toUname', 1, 'varchar(64) DEFAULT NULL');



