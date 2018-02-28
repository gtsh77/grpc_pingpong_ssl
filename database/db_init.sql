CREATE TABLE main (
	id serial,
	msg varchar(256)
);

INSERT INTO main (msg) VALUES ('PONG_FROM_DB');

CREATE USER pp_user WITH PASSWORD '123';
GRANT ALL PRIVILEGES ON TABLE "main" TO pp_user;