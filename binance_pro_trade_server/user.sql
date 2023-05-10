/******************************************/
/*   DatabaseName = real   */
/*   TableName = user   */
/******************************************/
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `account` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `registerTime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `usdtAssets` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '0',
  `loginTime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `binanceApiArr` json DEFAULT NULL,
  `hotKeyConfigObj` json DEFAULT NULL,
  `stateConfigObj` json DEFAULT NULL,
  `serverInfoObj` json DEFAULT NULL,
  `registerIP` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `accessToken` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `showSymbolObj` json DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `account` (`account`,`accessToken`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=184 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC
;
