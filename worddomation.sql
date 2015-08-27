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
-- Name: Player_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('"Player_id_seq"', 99, true);


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY task (id, name, description, custom_values) FROM stdin;
1	shooting	acquires accuracy	\N
3	assisting	helping allied players	\N
4	quiz solving	answer quiz questions	\N
5	base capturing	capture enemy bases	\N
6	base defense	defend own base	\N
2	survival	player avoids being hit	{}
\.


--
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY event (id, tid, name, description, score_points, score_interval, skill_points, skill_interval, custom_values, score_rule, skill_rule) FROM stdin;
14	4	correct answer	player answered question correctly	10	1	10	1	{"award": "easy"}	\N	\N
15	4	wrong answer	player answered question wrong	-10	1	-10	1	{"award": "damn it"}	\N	\N
16	4	streak	player answered 3 following questions correctly	10	1	5	1	{"award": "bring it on"}	\N	\N
19	4	genius	player answered 10 questions correctly	30	10	30	10	{"award": "is that all"}	\N	\N
18	4	slack	player answered 3 following questions wrong	-10	1	-5	1	{"award": "i was gonna say that"}	\N	\N
20	4	whoami	player answered 10 questions wrong	0	1	-30	10	{"award": "learning fakes the result"}	\N	\N
21	5	base captured	player caputered base	10	1	10	1	{"award": null}	\N	\N
22	5	base capturer	player captured 5 bases	10	5	10	5	{"award": "got it"}	\N	\N
24	6	base defended	player reclaimed own base after enemy started capturing	10	1	10	1	{"award": "not so fast"}	\N	\N
26	6	weak defender	player failed to defend the base	0	1	-20	2	{"award": "how dare you"}	\N	\N
25	6	base defender	player was in base when enemy tried to capture	5	1	10	1	{"award": "as long as i live"}	\N	\N
2	1	hit	player hits enemy player	1	10	10	1	{"award": "first hit"}	event__score_points * 10	event__skill_points * 10
13	3	lonely wolf	player was not assisting base capture	0	1	-10	10	{"award": "ahooo"}	\N	\N
6	1	teamhit	player hits allied player	0	1	-90	1	{"award": "get some glasses"}	\N	\N
27	1	neverhit	player misses 20 shots	0	1	-10	20	{"award": "better get some glasses"}	\N	\N
28	2	was hit	player was hit	0	1	-1	1	{}	\N	\N
23	5	hit in action	player was hit while trying to capture/ defend base	0	1	-5	1	{"award": "hia"}	\N	\N
12	3	base assist	player was within 50m range when base was captured	5	1	10	1	{"award": "right behind you"}	\N	\N
9	2	survivor	player is not hit twice within 30 seconds	100	1	20	1	{"award": "like a weasel"}	\N	\N
11	2	victim	player is hit twice within 15 seconds	0	1	-30	1	{"award": "take it easy"}	\N	\N
10	2	amateur	player is hit twice between 15 and 30 seconds	0	1	-10	1	{"award": null}	\N	\N
8	2	legendary	player is not hit the entire level	300	1	50	1	{"award": "legendary"}	\N	\N
\.


--
-- Name: event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('event_id_seq', 26, true);


--
-- Data for Name: level; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY level (id, name, description, custom_values) FROM stdin;
2	Icy Iceglades	Freezing like a refrigarator.	{"bases": 5, "vision": 0.4, "terrain": "ice"}
3	Woody Woodlands	Can you find the forest with all that trees?	{"bases": 7, "vision": 0.2, "terrain": "forrest"}
4	Banana Savanna	Monkeys and Fruits	{"terrain": "tropic", "level_types": ["2"]}
1	Desert Island	Lots of heat in this map.	{"bases": "3", "vision": 1, "terrain": "desert", "level_types": ["1", "2", "3"]}
\.


--
-- Name: level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('level_id_seq', 8, true);


--
-- Data for Name: level_type; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY level_type (id, name, description, custom_values) FROM stdin;
3	Shooter	The Player has to shoot enemies assuring his own survival.	\N
2	Capture the base	The Player has to capture bases and defend them.	\N
1	Quiz	The Player has to find the right answer.	\N
4	Map editing	The Player has to create his own map.	\N
\.


--
-- Name: level_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('level_type_id_seq', 1, false);


--
-- Data for Name: player; Type: TABLE DATA; Schema: public; Owner: user1
--

COPY player (id, custom_values, name) FROM stdin;
86	{"clan": null}	Player 3
85	{"clan": null}	Player 2
87	{"clan": null}	Player 4
88	{"clan": "WNX"}	Player 5
89	{"clan": null}	Player 6
84	{"clan": "PBE", "name": "Player 1", "nickname": "007"}	Player 1
\.


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user1
--

SELECT pg_catalog.setval('task_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--

