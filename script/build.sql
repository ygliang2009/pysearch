use search;
drop table if exists urllist;
create table urllist(
	id int(10) primary key not null auto_increment,
	url varchar(255) not null,
	title varchar(50) not null
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
create index url_idx on urllist(url);

drop table if exists wordlist;
create table wordlist(
	id int(10) primary key not null auto_increment,
	word varchar(20) not null
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
alter table wordlist add column type int(2) default 0;

create index word_idx on wordlist(word);


drop table if exists link;
create table link(
	id int(10) primary key not null auto_increment,
	fromid int(10) not null,
	toid int(10) not null
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop table if exists wordlocation;
create table wordlocation(
	id int(10) primary key not null auto_increment,
	urlid int(10) not null,
	wordid int(10) not null,
	location int(10) not null
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
create index wordid_idx on wordlocation(wordid);

drop table if exists linkwords;
create table linkwords(
	id int(10) primary key not null auto_increment,
	wordid int(10) not null,
	linkid int(10) not null
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
