
CREATE TABLE `two_way_messages` (
	 `id` smallint(3) AUTO_INCREMENT,
   	`two_way_message_from` varchar(24),
	`two_way_message_to` varchar(24),
	`two_way_message_text` varchar(255),
	`two_way_message_time` float,
	PRIMARY KEY(`id`)
);


