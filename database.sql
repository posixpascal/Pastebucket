drop table if exists pastes;
drop table if exists users;

create table pastes (
	id string primary key not null,
	title string not null,
	text string not null,
	private string not null,
	syntaxhighlight string not null,
	ip string not null,
	date string not null
);


create table users (
	id integer primary key autoincrement,
	username string not null,
	apikey string not null,
	password string not null,
	email string not null,
	friends string not null,
	favorites string not null
	
);
