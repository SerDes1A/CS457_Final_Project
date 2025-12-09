--
-- PostgreSQL database dump
--

\restrict CcJyJuR9wTCC3QZk7barmxZqtLVfqrtcgQxRmtBOKOhCWvNMtq5ihvMdWTHa5lB

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Club; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."Club" (club_id, name, description, created_at, activity_status) FROM stdin;
4	The American Institute of Aeronautics and Astronautics	No description provided.	2025-12-08 00:37:07.447846-08	Active
5	American Nuclear Society	No description provided.	2025-12-08 00:37:07.500924-08	Active
6	American Society of Civil Engineers	No description provided.	2025-12-08 00:37:07.554491-08	Active
7	American Society of Mechanical Engineers	No description provided.	2025-12-08 00:37:07.608238-08	Active
8	Biomedical Engineering Society	No description provided.	2025-12-08 00:37:07.661148-08	Active
9	Concrete Canoe	No description provided.	2025-12-08 00:37:07.71539-08	Active
11	Geowall	No description provided.	2025-12-08 00:37:07.819825-08	Active
12	Institute of Electrical and Electronics Engineers	No description provided.	2025-12-08 00:37:07.873705-08	Active
13	Institute of Transportation Engineers - University of Nevada, Reno student chapter	No description provided.	2025-12-08 00:37:07.927637-08	Active
14	Material Advantage Student Chapter	No description provided.	2025-12-08 00:37:07.980104-08	Active
15	Nevada Cyber Club	No description provided.	2025-12-08 00:37:08.031667-08	Active
16	Nevada Wolf Pack Racing	No description provided.	2025-12-08 00:37:08.084276-08	Active
17	Phi Sigma Rho	No description provided.	2025-12-08 00:37:08.137694-08	Active
18	Pi Tau Sigma - Nevada Reno Beta Nu	No description provided.	2025-12-08 00:37:08.189396-08	Active
19	Society of Hispanic Professional Engineers	No description provided.	2025-12-08 00:37:08.243775-08	Active
20	Society of Women Engineers	No description provided.	2025-12-08 00:37:08.297157-08	Active
21	Steel Bridge	No description provided.	2025-12-08 00:37:08.348545-08	Active
22	Student Maker Association	No description provided.	2025-12-08 00:37:08.402311-08	Active
23	UNR Aerospace Club	No description provided.	2025-12-08 00:37:08.454454-08	Active
24	Water Treatment	No description provided.	2025-12-08 00:37:08.508271-08	Active
3	American Institute of Chemical Engineers	Help students to prepare for their career in chemical engineering.	2025-12-08 00:37:07.395287-08	Active
25	Baking Club	Learn baking skills!	2025-12-08 02:03:12.405963-08	Active
\.


--
-- Data for Name: Event; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."Event" (event_id, club, name, description, start_datetime, end_datetime, location, created_at) FROM stdin;
1	3	Weekly Meeting	Regular weekly club meeting	2024-12-10 18:00:00-08	2024-12-10 19:30:00-08	Engineering Building Room 101	2025-12-08 00:46:46.51492-08
2	3	Project Workshop	Hands-on project building session	2024-12-15 14:00:00-08	2024-12-15 17:00:00-08	Maker Space	2025-12-08 00:46:46.517209-08
3	3	Welcome Night	Get to meet the club!	\N	\N	Student Union	2025-12-08 01:33:57.045606-08
4	3	test	test	2025-12-08 00:00:00-08	2025-12-08 00:00:00-08	\N	2025-12-08 01:47:15.3144-08
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."User" (user_id, school_email, password, first_name, last_name, role, created_at) FROM stdin;
2	aantes@unr.edu	$2b$12$fQpPb.qeJTobG0e/RCPIvuGdgYnLpQLo22yDPGN4vQOD5IcGfeWcS	arwen	antes	student	2025-12-07 23:41:35.126116-08
3	bbob@unr.edu	$2b$12$6EgvQ4WRepJDgZi9uRzAMuXs7tZkODrsu.omX6NZ7991dI0iPiUmS	billy	bob	student	2025-12-07 23:58:41.543693-08
4	jdoe@unr.edu	$2b$12$/OEQ1WGQfqrDpbekwZTMoOuR16nXKox28YRGe0FRWrYgs/oAmAZs.	john	doe	student	2025-12-08 00:31:34.768139-08
5	president@unr.edu	$2b$12$kI11LvxdcyJ.5o0zVSOQsuMVrx23qmA1itB9ilSIyqsEjWKuZ3bPG	Alex	President	student	2025-12-08 00:46:45.66244-08
6	officer@unr.edu	$2b$12$dT8wqiLEd6FzXoSjiL/CneeoDgo4CH36ig9d3o6ix7/hQanWWNdpW	Jamie	Officer	student	2025-12-08 00:46:45.875119-08
7	member@unr.edu	$2b$12$4by6Yl/urZLgDB9L6BaB0OPbLN6q6AKE5KK2dXqWvaX62Rk6FKBAi	Taylor	Member	student	2025-12-08 00:46:46.080762-08
8	regular@unr.edu	$2b$12$A3JwgE7UebZNUzFGQxNiVeb9iuiLGDlDcfqlxmXzWfgkk0jS650Ni	Casey	Regular	student	2025-12-08 00:46:46.293122-08
9	msolen@unr.edu	$2b$12$ggef9noDltfMQWntKoxwnOX68zTSRo3E/6KY7cJd4q6vjflqSz/72	Mei	Solen	student	2025-12-08 03:12:23.279482-08
11	jbob@unr.edu	$2b$12$.ZS8mVEgBOjbcM5JNlicbuo1oH1ei8HFN2Z.H2Ao3UTvN6KDzpaOK			student	2025-12-08 18:10:36.215489-08
12	billb@unr.edu	$2b$12$TUr6w8qmY0t84kv9AJN/l.nUGMIDZ6uWHY1nisVjr6ksY23N2j8Dy	bill	bob	student	2025-12-08 18:15:23.338152-08
\.


--
-- Data for Name: Attendance; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."Attendance" (attendance_id, event, "user", status, "time") FROM stdin;
1	1	6	Present	2025-12-08 23:33:32.104921-08
4	3	5	Present	2025-12-08 23:43:42.38467-08
5	2	5	Present	2025-12-08 23:46:31.145785-08
\.


--
-- Data for Name: Club Membership; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."Club Membership" (membership_id, clubid, userid, role, is_active, dues_paid) FROM stdin;
4	3	8	member	t	f
5	23	5	member	f	f
6	15	8	member	f	f
9	15	2	member	f	f
8	25	5	member	t	f
3	3	7	officer	t	f
2	3	6	member	t	f
7	25	2	president	t	t
1	3	5	president	t	t
\.


--
-- Data for Name: File Resource; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."File Resource" (file_id, club, source_url, created_at, name) FROM stdin;
4	3	International Travel Form	2025-12-08	https://www.unr.edu/main/pdfs/verified-accessible/divisions-offices/administration-finance/human-resources/hr-international-travel-form-1.pdf
\.


--
-- Data for Name: Task; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."Task" (task_id, club, title, description, due_date, created_at, updated_at, priority, status) FROM stdin;
2	3	Order supplies	Order materials for project workshop	2024-12-12	2025-12-08 00:46:46.521134-08	2025-12-08 00:46:46.521134-08	High	Not Started
4	3	test	test	2025-12-30	2025-12-08 01:53:42.464136-08	2025-12-08 01:53:42.464136-08	High	Not Started
5	25	Get Materials	buy materials for next meeting	2025-11-13	2025-12-08 03:42:39.2176-08	2025-12-08 03:42:39.2176-08	Medium	Not Started
7	25	Finish Baked Goods	finish up items before bake sale	2025-10-21	2025-12-08 19:29:47.613289-08	2025-12-08 19:29:47.613289-08	Medium	Not Started
6	25	Get Materials	\N	2025-09-30	2025-12-08 18:17:10.309474-08	2025-12-08 21:50:14.783403-08	Medium	Complete
1	3	Prepare meeting agenda	Create agenda for next week's meeting	2024-12-08	2025-12-08 00:46:46.518105-08	2025-12-08 23:47:14.257717-08	Medium	Complete
\.


--
-- Data for Name: Task Assignment; Type: TABLE DATA; Schema: public; Owner: chadmin
--

COPY public."Task Assignment" (assignment_id, task, "user", assigned_at) FROM stdin;
1	6	5	2025-12-08 21:40:47.062328
2	7	2	2025-12-08 21:51:08.468474
3	1	5	2025-12-08 23:49:40.823541
\.


--
-- Name: Attendance_attendance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Attendance_attendance_id_seq"', 5, true);


--
-- Name: Attendance_event_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Attendance_event_seq"', 1, false);


--
-- Name: Attendance_user_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Attendance_user_seq"', 1, false);


--
-- Name: Club Membership_clubid_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Club Membership_clubid_seq"', 1, false);


--
-- Name: Club Membership_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Club Membership_membership_id_seq"', 11, true);


--
-- Name: Club Membership_userid_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Club Membership_userid_seq"', 1, false);


--
-- Name: Club_club_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Club_club_id_seq"', 26, true);


--
-- Name: Event_club_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Event_club_seq"', 1, false);


--
-- Name: Event_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Event_event_id_seq"', 4, true);


--
-- Name: File Resource_club_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."File Resource_club_seq"', 1, false);


--
-- Name: File Resource_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."File Resource_file_id_seq"', 4, true);


--
-- Name: Task Assignment_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Task Assignment_assignment_id_seq"', 3, true);


--
-- Name: Task Assignment_task_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Task Assignment_task_seq"', 1, false);


--
-- Name: Task Assignment_user_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Task Assignment_user_seq"', 1, false);


--
-- Name: Task_club_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Task_club_seq"', 1, false);


--
-- Name: Task_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Task_task_id_seq"', 7, true);


--
-- Name: Users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chadmin
--

SELECT pg_catalog.setval('public."Users_user_id_seq"', 12, true);


--
-- PostgreSQL database dump complete
--

\unrestrict CcJyJuR9wTCC3QZk7barmxZqtLVfqrtcgQxRmtBOKOhCWvNMtq5ihvMdWTHa5lB

