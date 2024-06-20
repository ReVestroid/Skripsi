--CREATE TABLE DATA_GAMES(
--	rank_game int identity(1,1) PRIMARY KEY,
--	title varchar(225) NOT NULL,
--	price int ,
--	final_price int,
--);

--INSERT INTO DATA_GAMES
--VALUES
--	('Counter-Strike 2',0,0)

TRUNCATE Table DATA_GAMES

--ALTER TABLE DATA_GAMES
--ADD persen_disc float;

ALTER TABLE DATA_GAMES
ALTER COLUMN 
--price int;
--final_price int;
--persen_disc int;

SELECT * FROM DATA_GAMES
