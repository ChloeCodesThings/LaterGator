--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'LATIN1';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: facebookinfo; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE facebookinfo (
    facebookinfo_id integer NOT NULL,
    user_id integer NOT NULL,
    access_token character varying(200) NOT NULL,
    facebook_user_id character varying(200) NOT NULL
);


ALTER TABLE facebookinfo OWNER TO vagrant;

--
-- Name: facebookinfo_facebookinfo_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE facebookinfo_facebookinfo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE facebookinfo_facebookinfo_id_seq OWNER TO vagrant;

--
-- Name: facebookinfo_facebookinfo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE facebookinfo_facebookinfo_id_seq OWNED BY facebookinfo.facebookinfo_id;


--
-- Name: facebookpageposts; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE facebookpageposts (
    post_id integer NOT NULL,
    msg character varying(63206) NOT NULL,
    post_datetime integer NOT NULL,
    is_posted boolean NOT NULL,
    user_id integer NOT NULL,
    facebookinfo_id integer NOT NULL
);


ALTER TABLE facebookpageposts OWNER TO vagrant;

--
-- Name: facebookpageposts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE facebookpageposts_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE facebookpageposts_post_id_seq OWNER TO vagrant;

--
-- Name: facebookpageposts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE facebookpageposts_post_id_seq OWNED BY facebookpageposts.post_id;


--
-- Name: facebookposts; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE facebookposts (
    post_id integer NOT NULL,
    msg character varying(63206) NOT NULL,
    post_datetime integer NOT NULL,
    is_posted boolean NOT NULL,
    user_id integer NOT NULL,
    facebookinfo_id integer NOT NULL
);


ALTER TABLE facebookposts OWNER TO vagrant;

--
-- Name: facebookposts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE facebookposts_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE facebookposts_post_id_seq OWNER TO vagrant;

--
-- Name: facebookposts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE facebookposts_post_id_seq OWNED BY facebookposts.post_id;


--
-- Name: twitterinfo; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE twitterinfo (
    twitterinfo_id integer NOT NULL,
    user_id integer NOT NULL,
    oauth_token character varying(200) NOT NULL,
    oauth_token_secret character varying(200) NOT NULL
);


ALTER TABLE twitterinfo OWNER TO vagrant;

--
-- Name: twitterinfo_twitterinfo_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE twitterinfo_twitterinfo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE twitterinfo_twitterinfo_id_seq OWNER TO vagrant;

--
-- Name: twitterinfo_twitterinfo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE twitterinfo_twitterinfo_id_seq OWNED BY twitterinfo.twitterinfo_id;


--
-- Name: twitterposts; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE twitterposts (
    post_id integer NOT NULL,
    msg character varying(140) NOT NULL,
    post_datetime integer NOT NULL,
    is_posted boolean NOT NULL,
    user_id integer NOT NULL,
    twitterinfo_id integer NOT NULL
);


ALTER TABLE twitterposts OWNER TO vagrant;

--
-- Name: twitterposts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE twitterposts_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE twitterposts_post_id_seq OWNER TO vagrant;

--
-- Name: twitterposts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE twitterposts_post_id_seq OWNED BY twitterposts.post_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(20) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: facebookinfo_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookinfo ALTER COLUMN facebookinfo_id SET DEFAULT nextval('facebookinfo_facebookinfo_id_seq'::regclass);


--
-- Name: post_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookpageposts ALTER COLUMN post_id SET DEFAULT nextval('facebookpageposts_post_id_seq'::regclass);


--
-- Name: post_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookposts ALTER COLUMN post_id SET DEFAULT nextval('facebookposts_post_id_seq'::regclass);


--
-- Name: twitterinfo_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY twitterinfo ALTER COLUMN twitterinfo_id SET DEFAULT nextval('twitterinfo_twitterinfo_id_seq'::regclass);


--
-- Name: post_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY twitterposts ALTER COLUMN post_id SET DEFAULT nextval('twitterposts_post_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: facebookinfo; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY facebookinfo (facebookinfo_id, user_id, access_token, facebook_user_id) FROM stdin;
1	1	EAADWIW5YRKYBAHluhv67knLkOFopzq1ZCvklNertE1ZCrVwAirc0UbyyZBTqvAcko1lGQvY4vCwd1biR43QjLRmZBEsYqlM4HqOGKN4zU0czT6aI9VBHDQpycfj7YL5sIWoJgwAiWZCZBozjkuZAlspnxfZAB9FVGhc3jejDpzcLnQZDZD	10209868626926758
\.


--
-- Name: facebookinfo_facebookinfo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('facebookinfo_facebookinfo_id_seq', 1, true);


--
-- Data for Name: facebookpageposts; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY facebookpageposts (post_id, msg, post_datetime, is_posted, user_id, facebookinfo_id) FROM stdin;
1	hello world?	1484200800	f	1	1
2	hello world????	1484204400	f	1	1
3	this is a teeeeeest	1484200800	f	1	1
4	omg DOES THIS WORK?	1484222400	f	1	1
5	working???	1484200800	f	1	1
6	THIS WORKS!!!!!!!	1484200800	f	1	1
7	PRAISE RUPAUL!!!!!	1484226000	f	1	1
\.


--
-- Name: facebookpageposts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('facebookpageposts_post_id_seq', 7, true);


--
-- Data for Name: facebookposts; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY facebookposts (post_id, msg, post_datetime, is_posted, user_id, facebookinfo_id) FROM stdin;
\.


--
-- Name: facebookposts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('facebookposts_post_id_seq', 1, false);


--
-- Data for Name: twitterinfo; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY twitterinfo (twitterinfo_id, user_id, oauth_token, oauth_token_secret) FROM stdin;
\.


--
-- Name: twitterinfo_twitterinfo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('twitterinfo_twitterinfo_id_seq', 1, false);


--
-- Data for Name: twitterposts; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY twitterposts (post_id, msg, post_datetime, is_posted, user_id, twitterinfo_id) FROM stdin;
\.


--
-- Name: twitterposts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('twitterposts_post_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (user_id, username, password) FROM stdin;
1	chloe	$pbkdf2-sha256$29000$w/j/n9O6F8KY8x6jtDZmrA$W.qe1H4Xg7ReHGfPwWe1C7Hahgs9X/8uuABF05LhcjY
2	gfdgdfg	$pbkdf2-sha256$29000$HsN4j3FOqdV6bw0BYAzBmA$upEDcEsq1Ccw3F61CSTDfAVRO21Zhyx.Us94c/chtT0
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('users_user_id_seq', 2, true);


--
-- Name: facebookinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookinfo
    ADD CONSTRAINT facebookinfo_pkey PRIMARY KEY (facebookinfo_id);


--
-- Name: facebookpageposts_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookpageposts
    ADD CONSTRAINT facebookpageposts_pkey PRIMARY KEY (post_id);


--
-- Name: facebookposts_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookposts
    ADD CONSTRAINT facebookposts_pkey PRIMARY KEY (post_id);


--
-- Name: twitterinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY twitterinfo
    ADD CONSTRAINT twitterinfo_pkey PRIMARY KEY (twitterinfo_id);


--
-- Name: twitterposts_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY twitterposts
    ADD CONSTRAINT twitterposts_pkey PRIMARY KEY (post_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: facebookinfo_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookinfo
    ADD CONSTRAINT facebookinfo_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: facebookpageposts_facebookinfo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookpageposts
    ADD CONSTRAINT facebookpageposts_facebookinfo_id_fkey FOREIGN KEY (facebookinfo_id) REFERENCES facebookinfo(facebookinfo_id);


--
-- Name: facebookpageposts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookpageposts
    ADD CONSTRAINT facebookpageposts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: facebookposts_facebookinfo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookposts
    ADD CONSTRAINT facebookposts_facebookinfo_id_fkey FOREIGN KEY (facebookinfo_id) REFERENCES facebookinfo(facebookinfo_id);


--
-- Name: facebookposts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY facebookposts
    ADD CONSTRAINT facebookposts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: twitterinfo_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY twitterinfo
    ADD CONSTRAINT twitterinfo_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: twitterposts_twitterinfo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY twitterposts
    ADD CONSTRAINT twitterposts_twitterinfo_id_fkey FOREIGN KEY (twitterinfo_id) REFERENCES twitterinfo(twitterinfo_id);


--
-- Name: twitterposts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY twitterposts
    ADD CONSTRAINT twitterposts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

