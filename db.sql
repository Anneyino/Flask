CREATE DATABASE moelearn character set utf8;

USE moelearn

CREATE TABLE user(
    uid INT AUTO_INCREMENT,
    username VARCHAR(50) unique NOT NULL,
    passwd VARCHAR(50) NOT NULL, -- for security concern, this field should be the hash(i.e. SHA256) of actual password
    email VARCHAR(50),
    PRIMARY KEY(uid)
)charset=utf8;

CREATE TABLE friend(
    uid_primary INT,
    uid_secondary INT,
    PRIMARY KEY(uid_primary, uid_secondary),
    FOREIGN KEY(uid_primary) REFERENCES user(uid),
    FOREIGN KEY(uid_secondary) REFERENCES user(uid)
)charset=utf8;

CREATE TABLE helper(
    hid INT AUTO_INCREMENT,
    model_id INT,
    costume_id INT,
    PRIMARY KEY(hid)
)charset=utf8;

CREATE TABLE subject(
    sid INT AUTO_INCREMENT,
    full_name VARCHAR(50),
    chapter_no INT,
    store_path VARCHAR(100),
    PRIMARY KEY(sid)
)charset=utf8;

CREATE TABLE user_helper(
    uid INT,
    hid INT,
    relation INT,
    PRIMARY KEY(uid, hid),
    FOREIGN KEY(uid) REFERENCES user(uid),
    FOREIGN KEY(hid) REFERENCES helper(hid)
)charset=utf8;

CREATE TABLE user_subject(
    uid INT,
    sid INT,
    progress INT,
    PRIMARY KEY(uid, sid),
    FOREIGN KEY(uid) REFERENCES user(uid),
    FOREIGN KEY(sid) REFERENCES subject(sid)
)charset=utf8;

CREATE TABLE session(
    session_id INT,
    uid INT,
    created_time DATETIME DEFAULT NOW(), -- for security concern, session_id should only be valid for period of time
    PRIMARY KEY(session_id),
    FOREIGN KEY(uid) REFERENCES user(uid)
);

INSERT INTO subject VALUES(1, '英语', 90, 'Resources/english');