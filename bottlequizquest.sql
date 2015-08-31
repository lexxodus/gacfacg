--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY task (id, name, description, custom_values) FROM stdin;
1	Quiz solving	The player has to select the pictures of non alcoholic beverages from a set of beverages as fast as possible.	{}
\.


--
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY event (id, tid, name, description, score_points, score_rule, score_interval, skill_points, skill_rule, skill_interval, custom_values) FROM stdin;
1	1	answer given	player entered his solution	50	event__score_points + 50 * triggered_event__right_answers_amount - 25 * triggered_event__wrong_answers_amount - triggered_event__response_time	1	15	event__skill_points + 2 * triggered_event__right_answers_amount - triggered_event__wrong_answers_amount - triggered_event__response_time	1	{}
\.


--
-- Name: event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('event_id_seq', 1, true);


--
-- Data for Name: level; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY level (id, name, description, custom_values) FROM stdin;
2	Home	Let's get some refreshments from the fridge!	{"level_types": ["1"]}
3	Restaurant	Find yourself some beverages along a nice meal.	{"level_types": ["1"]}
1	Beverage Store	Can you find your way through this store's offers?	{"spots": "7", "level_types": ["1"], "pictures right": "path/to/picture/1, path/to/picture/2, path/to/picture/3, path/to/picture/4, path/to/picture/5, path/to/picture/6, path/to/picture/7, path/to/picture/8, path/to/picture/9, path/to/picture/10", "pictures wrong": "path/to/picture/11, path/to/picture/12, path/to/picture/13, path/to/picture/14, path/to/picture/15, path/to/picture/16, path/to/picture/17, path/to/picture/18, path/to/picture/19, path/to/picture/20, path/to/picture/21, path/to/picture/22, path/to/picture/23, path/to/picture/24, path/to/picture/25, path/to/picture/26, path/to/picture/27, path/to/picture/28, path/to/picture/29, path/to/picture/30"}
\.


--
-- Name: level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('level_id_seq', 3, true);


--
-- Data for Name: level_type; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY level_type (id, name, description, custom_values) FROM stdin;
1	Picture Quiz	The player has to select the pictures of non alcoholic beverages from a set of beverages.	{}
\.


--
-- Name: level_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('level_type_id_seq', 1, true);


--
-- Data for Name: player; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY player (id, name, custom_values) FROM stdin;
1	Checker	{"name": "Checker"}
2	Intermediate	{"name": "Intermediate"}
3	Noob	{"name": "Noob"}
\.


--
-- Name: player_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('player_id_seq', 3, true);


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('task_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

