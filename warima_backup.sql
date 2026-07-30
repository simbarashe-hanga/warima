--
-- PostgreSQL database dump
--

\restrict 5vxhrpwfuBruim8DDHJynm1WPpnaF9BzpgF4Sra9j8yLQI4HQZMwLgTMo0AaHd3

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.4 (Ubuntu 18.4-0ubuntu0.26.04.1)

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
-- Name: identityprovider; Type: TYPE; Schema: public; Owner: warima_user
--

CREATE TYPE public.identityprovider AS ENUM (
    'WHATSAPP',
    'EMAIL',
    'GOOGLE',
    'APPLE'
);


ALTER TYPE public.identityprovider OWNER TO warima_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO warima_user;

--
-- Name: conversation_messages; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.conversation_messages (
    id integer NOT NULL,
    user_id character varying,
    role character varying,
    content text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.conversation_messages OWNER TO warima_user;

--
-- Name: conversation_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: warima_user
--

CREATE SEQUENCE public.conversation_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.conversation_messages_id_seq OWNER TO warima_user;

--
-- Name: conversation_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: warima_user
--

ALTER SEQUENCE public.conversation_messages_id_seq OWNED BY public.conversation_messages.id;


--
-- Name: event_queue; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.event_queue (
    id integer NOT NULL,
    message_id character varying,
    user_id character varying,
    payload json,
    status character varying,
    attempts integer,
    error text,
    created_at timestamp without time zone
);


ALTER TABLE public.event_queue OWNER TO warima_user;

--
-- Name: event_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: warima_user
--

CREATE SEQUENCE public.event_queue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.event_queue_id_seq OWNER TO warima_user;

--
-- Name: event_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: warima_user
--

ALTER SEQUENCE public.event_queue_id_seq OWNED BY public.event_queue.id;


--
-- Name: processed_messages; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.processed_messages (
    message_id character varying NOT NULL
);


ALTER TABLE public.processed_messages OWNER TO warima_user;

--
-- Name: transactions; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.transactions (
    id character varying NOT NULL,
    user_id character varying,
    amount integer,
    status character varying,
    idempotency_key character varying
);


ALTER TABLE public.transactions OWNER TO warima_user;

--
-- Name: user_identities; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.user_identities (
    id uuid NOT NULL,
    user_id character varying NOT NULL,
    provider public.identityprovider NOT NULL,
    provider_identifier character varying NOT NULL,
    verified boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.user_identities OWNER TO warima_user;

--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.user_sessions (
    user_id character varying NOT NULL,
    state character varying,
    context json,
    last_seen character varying,
    expires_at character varying
);


ALTER TABLE public.user_sessions OWNER TO warima_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: warima_user
--

CREATE TABLE public.users (
    id character varying NOT NULL,
    user_id character varying,
    user_name character varying,
    status character varying,
    balance integer,
    message_id character varying
);


ALTER TABLE public.users OWNER TO warima_user;

--
-- Name: conversation_messages id; Type: DEFAULT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.conversation_messages ALTER COLUMN id SET DEFAULT nextval('public.conversation_messages_id_seq'::regclass);


--
-- Name: event_queue id; Type: DEFAULT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.event_queue ALTER COLUMN id SET DEFAULT nextval('public.event_queue_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.alembic_version (version_num) FROM stdin;
c4d9f426ccb9
\.


--
-- Data for Name: conversation_messages; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.conversation_messages (id, user_id, role, content, created_at) FROM stdin;
1	27672489700	user	hello	2026-07-01 10:34:55.149327+00
2	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-01 10:34:55.159024+00
3	16315551181	user	this is a text message	2026-07-08 00:54:33.95078+00
4	16315551181	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-08 00:54:33.964558+00
5	27672489700	user	hi	2026-07-08 01:14:02.763758+00
6	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-08 01:14:02.775931+00
7	27672489700	user	hi warima	2026-07-08 02:24:00.054852+00
8	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-08 02:24:00.084852+00
9	27672489700	user	hi warima	2026-07-08 16:15:02.861935+00
10	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-08 16:15:02.87829+00
11	27672489700	user	hello	2026-07-12 13:35:28.441403+00
12	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-12 13:35:28.459479+00
13	27672489700	user	contribute	2026-07-12 13:39:09.253598+00
14	27672489700	assistant	How much would you like to contribute?	2026-07-12 13:39:09.260284+00
15	27672489700	user	1000	2026-07-12 13:43:14.180485+00
16	27672489700	assistant	Confirm R1000? Reply 1 to confirm, 2 to cancel.	2026-07-12 13:43:14.187248+00
17	27672489700	user	1	2026-07-12 13:43:19.659038+00
18	27672489700	assistant	Contribution of R1000 received. Transaction ID: 77ef8260-3a6a-4dd1-8b4e-a01d352054e1	2026-07-12 13:43:19.67259+00
19	27672489700	user	thank you	2026-07-12 13:43:28.201507+00
20	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 13:43:28.209321+00
21	27672489700	user	hi warima	2026-07-12 18:59:02.746796+00
22	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 18:59:02.76066+00
23	27672489700	user	hi warima	2026-07-12 19:10:19.689586+00
24	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 19:10:19.697019+00
25	27672489700	user	contribute	2026-07-12 19:10:32.421441+00
26	27672489700	assistant	How much would you like to contribute?	2026-07-12 19:10:32.428448+00
27	27672489700	user	hi	2026-07-12 19:14:50.802781+00
28	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-12 19:14:50.810925+00
29	27672489700	user	hi warima	2026-07-12 19:47:00.61745+00
30	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 19:47:00.625002+00
31	27672489700	user	hi warima	2026-07-12 19:47:22.209917+00
32	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 19:47:22.217741+00
33	27672489700	user	contribute	2026-07-12 19:48:03.072124+00
34	27672489700	assistant	How much would you like to contribute?	2026-07-12 19:48:03.088133+00
35	27672489700	user	hi	2026-07-12 19:53:05.735377+00
36	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-12 19:53:05.744331+00
37	27672489700	user	contribute	2026-07-12 19:53:18.893839+00
38	27672489700	assistant	How much would you like to contribute?	2026-07-12 19:53:18.900437+00
39	27672489700	user	hi warima	2026-07-12 19:58:55.021187+00
40	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 19:58:55.033052+00
41	27672489700	user	contribute	2026-07-12 19:59:24.206958+00
42	27672489700	assistant	How much would you like to contribute?	2026-07-12 19:59:24.213451+00
43	27672489700	user	hi warima	2026-07-12 20:11:38.690759+00
44	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 20:11:38.703216+00
45	27672489700	user	contribute	2026-07-12 20:12:17.276641+00
46	27672489700	assistant	How much would you like to contribute?	2026-07-12 20:12:17.284091+00
47	27672489700	user	1000	2026-07-12 20:12:24.723285+00
48	27672489700	assistant	Confirm R1000? Reply 1 to confirm, 2 to cancel.	2026-07-12 20:12:24.730952+00
49	27672489700	user	2	2026-07-12 20:12:32.149647+00
50	27672489700	assistant	Cancelled. Type 'contribute' to start again.	2026-07-12 20:12:32.156774+00
51	27672489700	user	contribute	2026-07-12 20:12:42.67505+00
52	27672489700	assistant	How much would you like to contribute?	2026-07-12 20:12:42.681673+00
53	27672489700	user	1000	2026-07-12 20:12:51.20229+00
54	27672489700	assistant	Confirm R1000? Reply 1 to confirm, 2 to cancel.	2026-07-12 20:12:51.209534+00
55	27672489700	user	1	2026-07-12 20:12:58.694398+00
56	27672489700	assistant	Contribution of R1000 received. Transaction ID: 6c87cfbc-8c83-47d4-a883-c8f930418f93	2026-07-12 20:12:58.707272+00
57	27672489700	user	hi	2026-07-12 20:13:08.281963+00
58	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-12 20:13:08.288995+00
59	27672489700	user	agent	2026-07-12 20:13:29.808374+00
60	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-12 20:13:29.815196+00
61	27672489700	user	what is your name	2026-07-12 20:13:46.384703+00
62	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 20:13:46.392653+00
63	27672489700	user	agent	2026-07-12 20:14:03.558527+00
64	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-12 20:14:03.580181+00
65	27672489700	user	my balancr please	2026-07-12 20:14:19.090117+00
66	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 20:14:19.097717+00
67	27672489700	user	hi	2026-07-12 20:25:42.637148+00
68	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-12 20:25:42.645759+00
69	27672489700	user	contribute	2026-07-12 20:25:52.281483+00
70	27672489700	assistant	How much would you like to contribute?	2026-07-12 20:25:52.288275+00
71	27672489700	user	agent	2026-07-12 20:26:00.739465+00
72	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-12 20:26:00.747922+00
73	27672489700	user	contribute	2026-07-12 20:26:11.316328+00
74	27672489700	assistant	How much would you like to contribute?	2026-07-12 20:26:11.322943+00
75	27672489700	user	1000	2026-07-12 20:26:18.819002+00
76	27672489700	assistant	Confirm R1000? Reply 1 to confirm, 2 to cancel.	2026-07-12 20:26:18.825967+00
77	27672489700	user	agent	2026-07-12 20:26:28.258723+00
78	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-12 20:26:28.265673+00
79	27672489700	user	contribute	2026-07-12 20:26:38.804278+00
80	27672489700	assistant	How much would you like to contribute?	2026-07-12 20:26:38.810832+00
81	27672489700	user	1000	2026-07-12 20:26:47.272085+00
82	27672489700	assistant	Confirm R1000? Reply 1 to confirm, 2 to cancel.	2026-07-12 20:26:47.278974+00
83	27672489700	user	1	2026-07-12 20:26:59.713479+00
84	27672489700	assistant	Contribution of R1000 received. Transaction ID: 72e18005-b886-4473-a274-a816a81504c8	2026-07-12 20:26:59.724346+00
85	27672489700	user	hi, i want to start a stokvel with 10 members. how should we structure monthly contributions?	2026-07-12 20:27:55.444493+00
86	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-12 20:27:55.452392+00
87	27672489700	user	contribute	2026-07-13 10:04:09.61712+00
88	27672489700	assistant	How much would you like to contribute?	2026-07-13 10:04:09.624942+00
89	27672489700	user	agent	2026-07-13 10:04:31.387396+00
90	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-13 10:04:31.393777+00
91	27672489700	user	i want to start a stokvel	2026-07-13 10:06:30.418696+00
92	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 10:06:30.425354+00
93	27672489700	user	agent	2026-07-13 10:19:01.996856+00
94	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-13 10:19:02.041665+00
95	27672489700	user	hi warima	2026-07-13 10:38:15.462517+00
96	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 10:38:15.469233+00
97	27672489700	user	hi warima	2026-07-13 13:49:33.019673+00
98	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 13:49:33.031732+00
99	27672489700	user	contribute	2026-07-13 13:53:33.285858+00
100	27672489700	assistant	How much would you like to contribute?	2026-07-13 13:53:33.292441+00
101	27672489700	user	hi warima	2026-07-13 14:07:39.027248+00
102	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 14:07:39.039776+00
103	27672489700	user	balance	2026-07-13 14:08:35.516463+00
104	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 14:08:35.522993+00
105	27672489700	user	hi	2026-07-13 14:11:59.833236+00
106	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-13 14:11:59.843222+00
107	27672489700	user	agent	2026-07-13 14:12:09.430135+00
108	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-13 14:12:09.435932+00
109	27672489700	user	whats your name	2026-07-13 14:12:22.920585+00
110	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 14:12:22.928903+00
111	27672489700	user	what is your name	2026-07-13 14:24:40.586107+00
112	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 14:24:40.597802+00
113	27672489700	user	hello	2026-07-13 14:28:06.802672+00
114	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-13 14:28:06.813017+00
115	27672489700	user	agent	2026-07-13 14:28:17.337538+00
116	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-13 14:28:17.348307+00
117	27672489700	user	what is your name	2026-07-13 14:28:31.910836+00
118	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 14:28:31.918353+00
119	27672489700	user	hi warima	2026-07-13 14:30:23.368694+00
120	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 14:30:23.380161+00
121	27672489700	user	hi warima	2026-07-13 18:20:21.851178+00
122	27672489700	assistant	Warima AI is temporarily unavailable.Please try again shortly.	2026-07-13 18:20:21.863265+00
123	27672489700	user	hi warima	2026-07-14 05:44:09.328677+00
124	27672489700	assistant	I'm sorry, I'm having trouble processing your request at the moment. Please try again shortly.	2026-07-14 05:44:09.34436+00
125	27672489700	user	hi warima	2026-07-14 05:52:24.92281+00
126	27672489700	assistant	I'm Warima, your Stokvel assistant. How can I help you today?	2026-07-14 05:52:24.934568+00
127	27672489700	user	contibutions	2026-07-14 05:52:49.090189+00
128	27672489700	assistant	Let's talk about contributions. I can help you understand how they work in your Stokvel. What do you want to know?	2026-07-14 05:52:49.096693+00
129	27672489700	user	contribute	2026-07-14 05:53:00.156769+00
130	27672489700	assistant	How much would you like to contribute?	2026-07-14 05:53:00.166238+00
131	27672489700	user	1000	2026-07-14 05:53:07.661435+00
132	27672489700	assistant	Confirm R1000? Reply 1 to confirm, 2 to cancel.	2026-07-14 05:53:07.66804+00
133	27672489700	user	1	2026-07-14 05:53:13.105554+00
134	27672489700	assistant	Contribution of R1000 received. Transaction ID: b93ce77c-c68b-4dc3-b52b-16d5262757ad	2026-07-14 05:53:13.122116+00
135	27672489700	user	thank you	2026-07-14 06:10:20.775324+00
136	27672489700	assistant	You're welcome. Need help with anything else?	2026-07-14 06:10:20.782213+00
137	27672489700	user	no	2026-07-14 06:10:36.001042+00
138	27672489700	assistant	Have a great day!	2026-07-14 06:10:36.009114+00
139	27672489700	user	hi warima	2026-07-14 06:13:35.39767+00
140	27672489700	assistant	How can I help you today?	2026-07-14 06:13:35.404376+00
141	27672489700	user	contibution	2026-07-14 06:13:53.881685+00
142	27672489700	assistant	How much would you like to contribute?	2026-07-14 06:13:53.888444+00
143	27672489700	user	1000	2026-07-14 06:14:06.748314+00
144	27672489700	assistant	Confirm R1000? Reply 1 to confirm, 2 to cancel.	2026-07-14 06:14:06.754853+00
145	27672489700	user	1	2026-07-14 06:14:13.212441+00
146	27672489700	assistant	Contribution of R1000 received. Transaction ID: 4f21517d-22a6-4548-a379-b600cdbf6199	2026-07-14 06:14:13.222611+00
147	27672489700	user	agent	2026-07-14 06:14:22.699623+00
148	27672489700	assistant	You are chatting with the Warima A.I Agent	2026-07-14 06:14:22.705586+00
149	27672489700	user	tell me about contributions	2026-07-14 06:14:40.308776+00
150	27672489700	assistant	I'm sorry, I'm having trouble processing your request at the moment. Please try again shortly.	2026-07-14 06:14:40.315444+00
151	27672489700	user	are you there	2026-07-14 06:15:11.791586+00
152	27672489700	assistant	Yes, I'm here. Contributions are regular payments made to your Stokvel.	2026-07-14 06:15:11.798372+00
153	27672489700	user	how	2026-07-14 06:15:23.38526+00
154	27672489700	assistant	You make contributions by sending money to your Stokvel group. I can guide you.	2026-07-14 06:15:23.391714+00
155	27672489700	user	are you there	2026-07-14 06:15:59.035051+00
156	27672489700	assistant	Yes, I'm here to help with Stokvel questions.	2026-07-14 06:15:59.041894+00
157	27672489700	user	okay	2026-07-14 06:16:13.583956+00
158	27672489700	assistant	How can I assist you today?	2026-07-14 06:16:13.58986+00
159	27672489700	user	guide me	2026-07-14 06:16:24.85841+00
160	27672489700	assistant	Let's start with savings. What's your goal?	2026-07-14 06:16:24.86465+00
161	27672489700	user	cancel	2026-07-14 06:16:39.421479+00
162	27672489700	assistant	Alright, let's start fresh. Need help with Stokvel?	2026-07-14 06:16:39.427942+00
163	27672489700	user	bye	2026-07-14 06:16:54.782774+00
164	27672489700	assistant	Bye, stay financially fit!	2026-07-14 06:16:54.789043+00
165	27672489700	user	hi	2026-07-14 07:01:45.402487+00
166	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-14 07:01:45.4095+00
167	27738651439	user	hi	2026-07-14 08:59:36.407339+00
168	27738651439	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-14 08:59:36.411998+00
169	27738651439	user	hello	2026-07-14 09:00:02.825135+00
170	27738651439	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-14 09:00:02.865292+00
171	27738651439	user	are you there	2026-07-14 09:00:24.326895+00
172	27738651439	assistant	I'm here. How can I help with your Stokvel?	2026-07-14 09:00:24.332871+00
173	27738651439	user	hi warima	2026-07-14 09:01:05.161505+00
174	27738651439	assistant	Hello! Need help with saving or Stokvel contributions?	2026-07-14 09:01:05.168737+00
175	27672489700	user	hi warima	2026-07-14 09:03:00.356647+00
176	27672489700	assistant	What's on your mind about your Stokvel?	2026-07-14 09:03:00.363446+00
177	27738651439	user	hi	2026-07-14 09:03:29.39479+00
178	27738651439	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-14 09:03:29.400803+00
179	27738651439	user	test	2026-07-14 09:07:52.96449+00
180	27738651439	assistant	All good! How's your Stokvel going?	2026-07-14 09:07:52.970623+00
181	27738651439	user	contribute	2026-07-14 09:08:33.746063+00
182	27738651439	assistant	How much would you like to contribute?	2026-07-14 09:08:33.752687+00
183	27672489700	user	hi warima	2026-07-14 14:41:15.336345+00
184	27672489700	assistant	Need help with savings or Stokvel?	2026-07-14 14:41:15.343254+00
185	27672489700	user	hi	2026-07-14 18:59:36.854963+00
186	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-14 18:59:36.861358+00
187	27672489700	user	hi	2026-07-15 10:54:27.710817+00
188	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-15 10:54:27.718079+00
189	27672489700	user	hi	2026-07-16 11:26:24.109051+00
190	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-16 11:26:24.115522+00
191	27738651439	user	hi	2026-07-16 11:27:12.565544+00
192	27738651439	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-16 11:27:12.571672+00
193	27672489700	user	hi	2026-07-16 19:03:53.879444+00
194	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-16 19:03:53.886149+00
195	27672489700	user	hi there	2026-07-20 13:32:51.414109+00
196	27672489700	assistant	Hi! How can I help with your Stokvel today?	2026-07-20 13:32:51.431989+00
197	27672489700	user	wow, what is your name?	2026-07-20 13:33:14.744519+00
198	27672489700	assistant	I'm Warima, your Stokvel assistant!	2026-07-20 13:33:14.750399+00
199	27672489700	user	i want to know more about what a stokvel is	2026-07-20 13:33:37.235144+00
200	27672489700	assistant	A Stokvel is a group savings plan where members contribute & save together.	2026-07-20 13:33:37.25071+00
201	27672489700	user	wow, i want to contribute!	2026-07-20 13:34:00.406273+00
202	27672489700	assistant	How much would you like to contribute?	2026-07-20 13:34:00.412379+00
203	27672489700	user	200	2026-07-20 13:34:07.952925+00
204	27672489700	assistant	Confirm R200? Reply 1 to confirm, 2 to cancel.	2026-07-20 13:34:07.959243+00
205	27672489700	user	1	2026-07-20 13:34:14.454481+00
206	27672489700	assistant	Contribution of R200 received. Transaction ID: f72e85bc-8da2-42f4-99f5-8155573611ae	2026-07-20 13:34:14.468601+00
207	27672489700	user	thank you	2026-07-20 13:34:23.032346+00
208	27672489700	assistant	You're welcome! Need help with anything else?	2026-07-20 13:34:23.038272+00
209	27672489700	user	nope	2026-07-20 13:34:33.691515+00
210	27672489700	assistant	Have a great day!	2026-07-20 13:34:33.698169+00
211	27672489700	user	1	2026-07-20 18:42:59.850245+00
212	27672489700	assistant	No amount found. Do you want to chat with 'agent' or 'contribute'.	2026-07-20 18:42:59.856964+00
213	27672489700	user	contribute	2026-07-20 18:43:13.159185+00
214	27672489700	assistant	How much would you like to contribute?	2026-07-20 18:43:13.165334+00
215	27672489700	user	2000	2026-07-20 18:43:22.669577+00
216	27672489700	assistant	Confirm R2000? Reply 1 to confirm, 2 to cancel.	2026-07-20 18:43:22.675468+00
217	27672489700	user	2	2026-07-20 18:43:30.186072+00
218	27672489700	assistant	Cancelled. Type 'contribute' to start again.	2026-07-20 18:43:30.19244+00
219	27672489700	user	1	2026-07-20 18:43:37.696059+00
220	27672489700	assistant	No amount found. Do you want to chat with 'agent' or 'contribute'.	2026-07-20 18:43:37.70241+00
221	27672489700	user	contribute	2026-07-20 18:43:48.2848+00
222	27672489700	assistant	How much would you like to contribute?	2026-07-20 18:43:48.290905+00
223	27672489700	user	2000	2026-07-20 18:43:55.877413+00
224	27672489700	assistant	Confirm R2000? Reply 1 to confirm, 2 to cancel.	2026-07-20 18:43:55.883216+00
225	27672489700	user	1	2026-07-20 18:44:02.374626+00
226	27672489700	assistant	Contribution of R2000 received. Transaction ID: 4ff416af-14ef-403d-a8a9-75ddfd10a636	2026-07-20 18:44:02.398114+00
227	27672489700	user	hi warima	2026-07-26 06:22:34.618736+00
228	27672489700	assistant	Hello! How can I help you with your Stokvel today?	2026-07-26 06:22:34.636194+00
229	27672489700	user	balance	2026-07-26 06:22:54.979305+00
230	27672489700	assistant	I don't have your balance info. Check with your Stokvel admin.	2026-07-26 06:22:54.98587+00
231	27672489700	user	okay, what can you do?	2026-07-26 06:32:38.458384+00
232	27672489700	assistant	I help with saving, understanding contributions & withdrawals, and building healthy financial habits.	2026-07-26 06:32:38.465327+00
233	27672489700	user	how	2026-07-26 06:32:49.582597+00
234	27672489700	assistant	I explain actions and provide info to help you manage your Stokvel.	2026-07-26 06:32:49.588823+00
235	27672489700	user	manage it how	2026-07-26 06:33:14.029289+00
236	27672489700	assistant	I guide you on consistent saving, tracking contributions, and withdrawals.	2026-07-26 06:33:14.03614+00
237	27672489700	user	what is my name	2026-07-26 15:21:40.656477+00
238	27672489700	assistant	You're talking to me, Warima. I don't know your name.	2026-07-26 15:21:40.663627+00
239	27672489700	user	aws benefits for startups https://share.google/i79r5iuouk6bggtkj	2026-07-29 07:56:52.608417+00
240	27672489700	assistant	That's not related to Stokvel. I help with saving and finances.	2026-07-29 07:56:52.623568+00
241	27672489700	user	hi	2026-07-29 07:58:23.041598+00
242	27672489700	assistant	Hey! Type 'contribute' or 'agent' to get started.	2026-07-29 07:58:23.047938+00
243	27672489700	user	are you there	2026-07-29 07:58:24.625627+00
244	27672489700	assistant	Yes, I'm here to help with Stokvel.	2026-07-29 07:58:24.631453+00
\.


--
-- Data for Name: event_queue; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.event_queue (id, message_id, user_id, payload, status, attempts, error, created_at) FROM stdin;
17	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkFFOTFFOUVCOUM0NjU0NURDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkFFOTFFOUVCOUM0NjU0NURDAA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 19:48:02.576883
1	wamid.test123	27672489700	{"id": "wamid.test123", "user_id": "27672489700", "text": "hello"}	DONE	1	\N	2026-07-01 10:34:54.983897
11	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjMwQkU5M0Q0RTQxOTE2RjE4AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjMwQkU5M0Q0RTQxOTE2RjE4AA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-12 18:59:02.548732
2	ABGGFlA5Fpa	16315551181	{"id": "ABGGFlA5Fpa", "user_id": "16315551181", "text": "this is a text message"}	DONE	1	\N	2026-07-08 00:54:33.449082
3	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMkExOURCRUFBOTI1M0ZGRUM4AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMkExOURCRUFBOTI1M0ZGRUM4AA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-08 01:14:02.419296
4	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUY5QzhBQzM1MjkwMjREMkIxNzMzQTBFQUY4NTI0MQA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUY5QzhBQzM1MjkwMjREMkIxNzMzQTBFQUY4NTI0MQA=", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-08 02:23:59.193667
12	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTk3QzY5Rjk2N0VDQjc4REFGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTk3QzY5Rjk2N0VDQjc4REFGAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-12 19:10:19.578588
5	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTkxMThEQUYzMUU2NjkzRUY1NUYzQUUzQzZCNENFQQA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTkxMThEQUYzMUU2NjkzRUY1NUYzQUUzQzZCNENFQQA=", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-08 16:15:02.448172
6	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUEwMzVFODNBQTA2MDJEODYwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUEwMzVFODNBQTA2MDJEODYwAA==", "user_id": "27672489700", "text": "hello"}	DONE	1	\N	2026-07-12 13:35:27.698326
7	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTlEMDY1MEYyN0MyODJCQkY0AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTlEMDY1MEYyN0MyODJCQkY0AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 13:39:08.378418
13	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTZDRkEzMzc4RjA3M0ZDREE2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTZDRkEzMzc4RjA3M0ZDREE2AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 19:10:31.763842
8	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzdFMUM3RDdDNEY2NTNDMzZFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzdFMUM3RDdDNEY2NTNDMzZFAA==", "user_id": "27672489700", "text": "1000"}	DONE	1	\N	2026-07-12 13:43:13.502667
9	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjA1NTJEMjRDNzUwMzMzQkExAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjA1NTJEMjRDNzUwMzMzQkExAA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-12 13:43:19.159395
18	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTExQjY3MzNCNDM3ODlDNzM1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTExQjY3MzNCNDM3ODlDNzM1AA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-12 19:53:05.312187
10	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzU1MzQ5M0FGQUU1RUVBQjk5AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzU1MzQ5M0FGQUU1RUVBQjk5AA==", "user_id": "27672489700", "text": "thank you"}	DONE	1	\N	2026-07-12 13:43:28.039359
14	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjE1NDdCQjg3MzI2RTA4QTNFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjE1NDdCQjg3MzI2RTA4QTNFAA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-12 19:14:50.626762
15	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODI3QUIzQkM4REUzMjlFRkZGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODI3QUIzQkM4REUzMjlFRkZGAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-12 19:46:59.864153
16	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQUNDNUNEMTMxN0IzQjhCRkE0AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQUNDNUNEMTMxN0IzQjhCRkE0AA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-12 19:47:21.216905
22	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkNGREJFMUFDNDE5QTNBRjBGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkNGREJFMUFDNDE5QTNBRjBGAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-12 20:11:37.898971
19	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzNFMzQ3NzY1MjNFNzQ5RUQyAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzNFMzQ3NzY1MjNFNzQ5RUQyAA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 19:53:18.756672
20	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjJERTg1N0I2Qjc4QzY2MTBCAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjJERTg1N0I2Qjc4QzY2MTBCAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-12 19:58:54.429527
21	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTcxMjI1QjRENjAxNEZGNTI0AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTcxMjI1QjRENjAxNEZGNTI0AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 19:59:23.245088
23	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNTg4MkJBQTAzMTU1M0ZGREY2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNTg4MkJBQTAzMTU1M0ZGREY2AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 20:12:16.730045
25	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTcxQzY5QUY1QUVDM0RDOTRFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTcxQzY5QUY1QUVDM0RDOTRFAA==", "user_id": "27672489700", "text": "2"}	DONE	1	\N	2026-07-12 20:12:31.92526
24	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzk5Njg4RTZCRkE1RkI0RTQ2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzk5Njg4RTZCRkE1RkI0RTQ2AA==", "user_id": "27672489700", "text": "1000"}	DONE	1	\N	2026-07-12 20:12:24.384408
26	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjgwOEFCMkIyRjIzNTM0MjQ4AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjgwOEFCMkIyRjIzNTM0MjQ4AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 20:12:41.996688
27	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwN0UyMzE5Mzc0MUM3N0I2MkE0AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwN0UyMzE5Mzc0MUM3N0I2MkE0AA==", "user_id": "27672489700", "text": "1000"}	DONE	1	\N	2026-07-12 20:12:50.581746
28	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjUzMkEzMUE2NDc2RENBNkI1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjUzMkEzMUE2NDc2RENBNkI1AA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-12 20:12:58.161682
29	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQ0M4Qjg5NzY0RDZERkU0QUZDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQ0M4Qjg5NzY0RDZERkU0QUZDAA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-12 20:13:07.464564
30	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTU3QjE1MzkxOTg5NUY4RDQyAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTU3QjE1MzkxOTg5NUY4RDQyAA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-12 20:13:29.056697
31	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzBCNUZBRjJERjcyRDQ4ODkzAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzBCNUZBRjJERjcyRDQ4ODkzAA==", "user_id": "27672489700", "text": "what is your name"}	DONE	1	\N	2026-07-12 20:13:45.613403
32	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTFEMDcyODFGNDZFMzU2NTA1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTFEMDcyODFGNDZFMzU2NTA1AA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-12 20:14:03.385799
33	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOERGOEIxQkNENUMwMzYyRjdFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOERGOEIxQkNENUMwMzYyRjdFAA==", "user_id": "27672489700", "text": "my balancr please"}	DONE	1	\N	2026-07-12 20:14:19.055317
34	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwREQ4N0EzNDRGMTVBNEU3NkZFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwREQ4N0EzNDRGMTVBNEU3NkZFAA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-12 20:25:42.439641
35	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjFCRENBRDY5M0I4QTYwNEM3AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjFCRENBRDY5M0I4QTYwNEM3AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 20:25:51.305658
36	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODE2ODNCMTY0NjBBNEQ4MzA1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODE2ODNCMTY0NjBBNEQ4MzA1AA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-12 20:25:59.764716
48	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUI1RUM5OTU0MDFERkM2MTI5AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUI1RUM5OTU0MDFERkM2MTI5AA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-13 10:38:14.601717
37	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjZCMDcwNjBFQjE2RjhENzZDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjZCMDcwNjBFQjE2RjhENzZDAA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 20:26:10.797666
43	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkY2NkQwRkQ1QzI5NTNBNkMzAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkY2NkQwRkQ1QzI5NTNBNkMzAA==", "user_id": "27672489700", "text": "hi, i want to start a stokvel with 10 members. how should we structure monthly contributions?"}	DONE	1	\N	2026-07-12 20:27:54.66064
38	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUYyNUYzNTBBRkEwMkVEMEE0AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUYyNUYzNTBBRkEwMkVEMEE0AA==", "user_id": "27672489700", "text": "1000"}	DONE	1	\N	2026-07-12 20:26:18.623575
39	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjkxQzBBNTg2MjgwNzMzNzJCAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjkxQzBBNTg2MjgwNzMzNzJCAA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-12 20:26:27.537476
40	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTUxREFERkE1MjYxODhFMUE2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTUxREFERkE1MjYxODhFMUE2AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-12 20:26:38.505495
44	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTBCNTgyQzQ0RjY1QjAxRDEwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTBCNTgyQzQ0RjY1QjAxRDEwAA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-13 10:04:09.508506
41	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDNCQkMzMzk2QUVFMzg0NDQ1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDNCQkMzMzk2QUVFMzg0NDQ1AA==", "user_id": "27672489700", "text": "1000"}	DONE	1	\N	2026-07-12 20:26:46.303366
42	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTdDRkE4MDMxM0VCNzNBOTYzAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTdDRkE4MDMxM0VCNzNBOTYzAA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-12 20:26:59.540677
49	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODNCNEEyRTM1MjlDRDBCM0ZDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODNCNEEyRTM1MjlDRDBCM0ZDAA==", "user_id": "27672489700", "text": "hello"}	PROCESSING	1	\N	2026-07-13 13:07:35.367791
45	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUUwQkJCMzBERDYxNjVFMzM3AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUUwQkJCMzBERDYxNjVFMzM3AA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-13 10:04:30.901495
46	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTNGMEQ1MEMzMkQ4NEQ3OTlEAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTNGMEQ1MEMzMkQ4NEQ3OTlEAA==", "user_id": "27672489700", "text": "i want to start a stokvel"}	DONE	1	\N	2026-07-13 10:06:29.462905
50	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzVFRDM5RTRDMUQ5NEEzMUZDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzVFRDM5RTRDMUQ5NEEzMUZDAA==", "user_id": "27672489700", "text": "hi warima"}	PROCESSING	1	\N	2026-07-13 13:33:10.139941
47	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNThEODI5NEQ5RTFGMDlDMEY1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNThEODI5NEQ5RTFGMDlDMEY1AA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-13 10:19:01.872894
53	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkU5MTBDMTk5NDVDRDgyNjRCAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkU5MTBDMTk5NDVDRDgyNjRCAA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-13 13:53:32.755716
51	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjYwNDU1QjlDMjEyRDQ1MkMwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjYwNDU1QjlDMjEyRDQ1MkMwAA==", "user_id": "27672489700", "text": "hi"}	PROCESSING	1	\N	2026-07-13 13:46:13.145804
52	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzQ2QUU2RENFNDYwQjEyQzNFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzQ2QUU2RENFNDYwQjEyQzNFAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-13 13:49:32.985536
55	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOEQyOURCMjVBQTExMDFCN0Y4AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOEQyOURCMjVBQTExMDFCN0Y4AA==", "user_id": "27672489700", "text": "balance"}	DONE	1	\N	2026-07-13 14:08:35.471791
54	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTA4ODc1NzA0RjNDRUIxNEJBAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTA4ODc1NzA0RjNDRUIxNEJBAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-13 14:07:38.353482
57	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMDg5RUU3NTAwMkM5OTY1RUQxAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMDg5RUU3NTAwMkM5OTY1RUQxAA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-13 14:12:09.422528
56	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjM1NjczMzEzRDc2QkIwQTMyAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjM1NjczMzEzRDc2QkIwQTMyAA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-13 14:11:59.43102
58	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUIwQTg1MkI1QjM5RTNENzM2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUIwQTg1MkI1QjM5RTNENzM2AA==", "user_id": "27672489700", "text": "whats your name"}	DONE	1	\N	2026-07-13 14:12:22.402583
59	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTMwNEQwOUEyQTlEQTQwRTk5AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTMwNEQwOUEyQTlEQTQwRTk5AA==", "user_id": "27672489700", "text": "what is your name"}	DONE	1	\N	2026-07-13 14:24:40.531975
60	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMEYxRTUwNkNBOEU2QjZCN0FGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMEYxRTUwNkNBOEU2QjZCN0FGAA==", "user_id": "27672489700", "text": "hello"}	DONE	1	\N	2026-07-13 14:28:06.481371
61	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjgzODI2MjJGNjcyOTlDRDIwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjgzODI2MjJGNjcyOTlDRDIwAA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-13 14:28:16.8548
62	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjVDMDFGQ0EyMDEzMkNCODY3AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjVDMDFGQ0EyMDEzMkNCODY3AA==", "user_id": "27672489700", "text": "what is your name"}	DONE	1	\N	2026-07-13 14:28:31.828818
63	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMDM4NTY5QUFDNDQ3NzBEQkE1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMDM4NTY5QUFDNDQ3NzBEQkE1AA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-13 14:30:23.171718
64	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzdDQzI4QzdDNTk3ODBBNjMzAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzdDQzI4QzdDNTk3ODBBNjMzAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-13 18:20:21.43749
72	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNTdGMDBBNTYzQUREMUI4RTlGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNTdGMDBBNTYzQUREMUI4RTlGAA==", "user_id": "27672489700", "text": "no"}	DONE	1	\N	2026-07-14 06:10:35.443579
65	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkM0OEJENDQzMzkwNjM0RDJBAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkM0OEJENDQzMzkwNjM0RDJBAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-13 20:09:20.694311
66	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzAzNUY4MzRDMzEzOTQ0NzFCAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzAzNUY4MzRDMzEzOTQ0NzFCAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-14 05:52:24.287445
78	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjFGNjI3RDZBNkQ4OTQ4MTI4AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjFGNjI3RDZBNkQ4OTQ4MTI4AA==", "user_id": "27672489700", "text": "tell me about contributions"}	DONE	1	\N	2026-07-14 06:14:40.05734
67	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTZGQkRCNzA3MzBEQTUwM0QxAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTZGQkRCNzA3MzBEQTUwM0QxAA==", "user_id": "27672489700", "text": "contibutions"}	DONE	1	\N	2026-07-14 05:52:48.189384
73	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjZGOTlGNzIxNTQxQkVBM0ZGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjZGOTlGNzIxNTQxQkVBM0ZGAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-14 06:13:34.557205
68	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNDU0OTVBMkM4QjgxQzM4QkQ3AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNDU0OTVBMkM4QjgxQzM4QkQ3AA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-14 05:52:59.817175
69	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTAxNTU5MTIwREVEMzE4OEMwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTAxNTU5MTIwREVEMzE4OEMwAA==", "user_id": "27672489700", "text": "1000"}	DONE	1	\N	2026-07-14 05:53:06.656698
70	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjdBQzhCQ0Y4QkJENDVEMTNGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjdBQzhCQ0Y4QkJENDVEMTNGAA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-14 05:53:12.41618
74	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQUYxNjlCNUE5QjgwRTY5RUZFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQUYxNjlCNUE5QjgwRTY5RUZFAA==", "user_id": "27672489700", "text": "contibution"}	DONE	1	\N	2026-07-14 06:13:53.203626
71	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOEI2MzhGNzhFQTdBNERGOTJGAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOEI2MzhGNzhFQTdBNERGOTJGAA==", "user_id": "27672489700", "text": "thank you"}	DONE	1	\N	2026-07-14 06:10:20.570526
82	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzIxODEwNzJGOTdCNUYyNDI0AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzIxODEwNzJGOTdCNUYyNDI0AA==", "user_id": "27672489700", "text": "okay"}	DONE	1	\N	2026-07-14 06:16:12.68718
75	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjYzMTBFQzJBMEIzRjVGOUI4AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjYzMTBFQzJBMEIzRjVGOUI4AA==", "user_id": "27672489700", "text": "1000"}	DONE	1	\N	2026-07-14 06:14:05.992889
79	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzc5RjA1OUE4RUY1OUE0QjA2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzc5RjA1OUE4RUY1OUE0QjA2AA==", "user_id": "27672489700", "text": "are you there"}	DONE	1	\N	2026-07-14 06:15:11.446178
76	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjZCRjYwRDA1MDVDMTM1RkNDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjZCRjYwRDA1MDVDMTM1RkNDAA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-14 06:14:13.031005
77	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkI1MkExNzAwNDRGMzdEODJDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkI1MkExNzAwNDRGMzdEODJDAA==", "user_id": "27672489700", "text": "agent"}	DONE	1	\N	2026-07-14 06:14:22.413593
80	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNkVFNkJGNzU4MzY2QURGNThCAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNkVFNkJGNzU4MzY2QURGNThCAA==", "user_id": "27672489700", "text": "how"}	DONE	1	\N	2026-07-14 06:15:22.873175
81	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTIzNDEwMDU3MDVFNTQ3RUYwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTIzNDEwMDU3MDVFNTQ3RUYwAA==", "user_id": "27672489700", "text": "are you there"}	DONE	1	\N	2026-07-14 06:15:50.625078
83	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTE3QTA1MjhEOUI4MTlFMDZBAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTE3QTA1MjhEOUI4MTlFMDZBAA==", "user_id": "27672489700", "text": "guide me"}	DONE	1	\N	2026-07-14 06:16:24.215234
85	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwREEwRTJGNDNGMkVERjBCRTBFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwREEwRTJGNDNGMkVERjBCRTBFAA==", "user_id": "27672489700", "text": "bye"}	DONE	1	\N	2026-07-14 06:16:53.778088
84	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkQ3QUVDMjE3MzUwRkVEQzI2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkQ3QUVDMjE3MzUwRkVEQzI2AA==", "user_id": "27672489700", "text": "cancel"}	DONE	1	\N	2026-07-14 06:16:39.298785
86	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODVEODEyNjZBODcxNkYzRTM1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODVEODEyNjZBODcxNkYzRTM1AA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-14 07:01:44.714932
87	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzE2NUFGNDIzNTVCNkIxRDBDODVCMTk0NDQ1MzM3QQA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzE2NUFGNDIzNTVCNkIxRDBDODVCMTk0NDQ1MzM3QQA=", "user_id": "27738651439", "text": "hi"}	DONE	1	\N	2026-07-14 08:59:36.184972
88	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQ0ZGMjY0Rjk4MzRENDRBM0MzMUZFRDYyMkZENTgwNAA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQ0ZGMjY0Rjk4MzRENDRBM0MzMUZFRDYyMkZENTgwNAA=", "user_id": "27738651439", "text": "hello"}	DONE	1	\N	2026-07-14 09:00:02.283988
89	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzFBMTQ1NjBBNjg0NjlERDY3NUY0OTZCNjY5NEM2NQA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzFBMTQ1NjBBNjg0NjlERDY3NUY0OTZCNjY5NEM2NQA=", "user_id": "27738651439", "text": "are you there"}	DONE	1	\N	2026-07-14 09:00:23.922291
90	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzhCMTBCMDEwNzI4ODAzMTJBMURCQUIxNTRCQjA3RgA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzhCMTBCMDEwNzI4ODAzMTJBMURCQUIxNTRCQjA3RgA=", "user_id": "27738651439", "text": "hi warima"}	DONE	1	\N	2026-07-14 09:01:04.756202
92	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzg5MEVFNEQyOEY1OENDMTA1Rjc3NDcyRTk2REQ1RAA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzg5MEVFNEQyOEY1OENDMTA1Rjc3NDcyRTk2REQ1RAA=", "user_id": "27738651439", "text": "hi"}	DONE	1	\N	2026-07-14 09:03:29.22898
91	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTk2QzNDNTZEQzVGMEEyOUZBOTJFRjUwNjRFQjM5OQA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTk2QzNDNTZEQzVGMEEyOUZBOTJFRjUwNjRFQjM5OQA=", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-14 09:02:59.504422
112	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwM0JCNTc0N0QxNTgwNDdBOUI5AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwM0JCNTc0N0QxNTgwNDdBOUI5AA==", "user_id": "27672489700", "text": "2"}	DONE	1	\N	2026-07-20 18:43:30.033094
93	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQ0MxMTY4REU0MDYyN0ZEQkY0N0FCMDJEM0YyOUY1RgA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQ0MxMTY4REU0MDYyN0ZEQkY0N0FCMDJEM0YyOUY1RgA=", "user_id": "27738651439", "text": "test"}	DONE	1	\N	2026-07-14 09:07:52.48706
102	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkJDNzMwN0FFNUZFRUMzRjU0AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkJDNzMwN0FFNUZFRUMzRjU0AA==", "user_id": "27672489700", "text": "wow, what is your name?"}	DONE	1	\N	2026-07-20 13:33:14.170155
94	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzE0MDg0NzdENjk2QUIxMUYxNTMwOEZGN0JGQjVEOQA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzE0MDg0NzdENjk2QUIxMUYxNTMwOEZGN0JGQjVEOQA=", "user_id": "27738651439", "text": "contribute"}	DONE	1	\N	2026-07-14 09:08:33.604007
95	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzQ3OEMwQ0QwMkQwQUU1RDFCAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzQ3OEMwQ0QwMkQwQUU1RDFCAA==", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-14 14:41:14.687032
108	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjA0NEI0OTgxNjMxQTYwN0M3AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjA0NEI0OTgxNjMxQTYwN0M3AA==", "user_id": "27672489700", "text": "nope"}	DONE	1	\N	2026-07-20 13:34:33.677159
96	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDkwMjlDMDREMjQ2NzBCNzRBAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDkwMjlDMDREMjQ2NzBCNzRBAA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-14 18:59:35.868684
103	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUIyM0YyNkZBNERCQkI2MkVDAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUIyM0YyNkZBNERCQkI2MkVDAA==", "user_id": "27672489700", "text": "i want to know more about what a stokvel is"}	DONE	1	\N	2026-07-20 13:33:36.65418
97	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMkFCQzA3QTJENTc2MkI2RDcwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMkFCQzA3QTJENTc2MkI2RDcwAA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-15 10:54:27.033102
98	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjIwOTY2NkYzMzZFNjg3MjU3AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjIwOTY2NkYzMzZFNjg3MjU3AA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-16 11:26:23.492266
99	wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzNEOTU3QTEwQTNBOEVFMDYwNjRFQzIyMkNFNzI3MQA=	27738651439	{"id": "wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzNEOTU3QTEwQTNBOEVFMDYwNjRFQzIyMkNFNzI3MQA=", "user_id": "27738651439", "text": "hi"}	DONE	1	\N	2026-07-16 11:27:12.343825
104	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMEJFQThCNzY5QUU2RkI0QTYzAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMEJFQThCNzY5QUU2RkI0QTYzAA==", "user_id": "27672489700", "text": "wow, i want to contribute!"}	DONE	1	\N	2026-07-20 13:34:00.197021
100	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzVGRTFGNEY2NUU4QkUwOTY2AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzVGRTFGNEY2NUU4QkUwOTY2AA==", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-16 19:03:53.834907
101	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNEJENUMxNTFFNkQzM0RCMzYzAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNEJENUMxNTFFNkQzM0RCMzYzAA==", "user_id": "27672489700", "text": "hi there"}	DONE	1	\N	2026-07-20 13:32:51.135616
105	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjFDQkQxOUI0RDIwMjgzRjZBAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjFDQkQxOUI0RDIwMjgzRjZBAA==", "user_id": "27672489700", "text": "200"}	DONE	1	\N	2026-07-20 13:34:07.621253
109	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjE2MjU2MkUxODkzREVCMEFCAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjE2MjU2MkUxODkzREVCMEFCAA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-20 18:42:59.095569
106	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjlGOUIwOTFFMzQ0Qzc2MUJEAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjlGOUIwOTFFMzQ0Qzc2MUJEAA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-20 13:34:14.310993
107	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDU0NUE1QjgxOUNGMkY1MDQ3AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDU0NUE1QjgxOUNGMkY1MDQ3AA==", "user_id": "27672489700", "text": "thank you"}	DONE	1	\N	2026-07-20 13:34:22.471371
115	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTUwNUQwNjczRUNCRUMzNTZFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTUwNUQwNjczRUNCRUMzNTZFAA==", "user_id": "27672489700", "text": "2000"}	DONE	1	\N	2026-07-20 18:43:55.763409
110	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkYwOEIzQjg5MzQxQjg2QzJBAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkYwOEIzQjg5MzQxQjg2QzJBAA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-20 18:43:12.646669
113	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRUM1MEYzQzA5ODU3QTczRjQ5AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRUM1MEYzQzA5ODU3QTczRjQ5AA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-20 18:43:36.954475
111	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODJDMDYxOUQ4M0U4QkM0Q0E1AA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODJDMDYxOUQ4M0U4QkM0Q0E1AA==", "user_id": "27672489700", "text": "2000"}	DONE	1	\N	2026-07-20 18:43:22.545946
117	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUI4QzBEMDREMkMyNDJBNTkzQUFBREQ2ODk2RDQ0NgA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUI4QzBEMDREMkMyNDJBNTkzQUFBREQ2ODk2RDQ0NgA=", "user_id": "27672489700", "text": "hi warima"}	DONE	1	\N	2026-07-26 06:22:33.653223
114	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNDgwNkE4MjM1QUE0M0RBQTAwAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNDgwNkE4MjM1QUE0M0RBQTAwAA==", "user_id": "27672489700", "text": "contribute"}	DONE	1	\N	2026-07-20 18:43:47.884449
116	wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNkZDMjZCOTQyNTJDN0Q0NjZFAA==	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNkZDMjZCOTQyNTJDN0Q0NjZFAA==", "user_id": "27672489700", "text": "1"}	DONE	1	\N	2026-07-20 18:44:01.633359
118	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTdCN0ZCMTlEMkUxODREOThDRkI2QjBDQzlDMzg3RgA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTdCN0ZCMTlEMkUxODREOThDRkI2QjBDQzlDMzg3RgA=", "user_id": "27672489700", "text": "balance"}	DONE	1	\N	2026-07-26 06:22:53.995188
119	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTc4MzM4MTY1MEQwQUU4MDM0MDlCNDkwOEM4RjExRAA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTc4MzM4MTY1MEQwQUU4MDM0MDlCNDkwOEM4RjExRAA=", "user_id": "27672489700", "text": "okay, what can you do?"}	DONE	1	\N	2026-07-26 06:32:38.098725
120	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTQ0NTdEN0JCNjk3ODVBNjhBNEZEQTlEMjJCQzlCMQA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTQ0NTdEN0JCNjk3ODVBNjhBNEZEQTlEMjJCQzlCMQA=", "user_id": "27672489700", "text": "how"}	DONE	1	\N	2026-07-26 06:32:49.101809
121	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUVGQUFDNUM4NDE1OUIxN0I4NzE0REM0N0MwNDUwRAA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUVGQUFDNUM4NDE1OUIxN0I4NzE0REM0N0MwNDUwRAA=", "user_id": "27672489700", "text": "manage it how"}	DONE	1	\N	2026-07-26 06:33:13.282694
122	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUJBODcxNDNBOUFENTlCOTdGNDM4RDUzOTE4NUU1RQA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUJBODcxNDNBOUFENTlCOTdGNDM4RDUzOTE4NUU1RQA=", "user_id": "27672489700", "text": "what is my name"}	DONE	1	\N	2026-07-26 15:21:40.031665
123	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTcwREVDRDI5OTg5NjY0QTNEMDFGRDQxMEJENkRBRAA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTcwREVDRDI5OTg5NjY0QTNEMDFGRDQxMEJENkRBRAA=", "user_id": "27672489700", "text": "aws benefits for startups https://share.google/i79r5iuouk6bggtkj"}	DONE	1	\N	2026-07-29 07:56:51.824124
124	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTNGQjhDMkQ1NUNGQjI2QTlCN0Q0MTU0QkY5MEM0MQA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTNGQjhDMkQ1NUNGQjI2QTlCN0Q0MTU0QkY5MEM0MQA=", "user_id": "27672489700", "text": "hi"}	DONE	1	\N	2026-07-29 07:57:44.422025
125	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUJGOTRGQjRFMjQ2MDkyNjI3MTRBRTBFRkM1QTU0QgA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUJGOTRGQjRFMjQ2MDkyNjI3MTRBRTBFRkM1QTU0QgA=", "user_id": "27672489700", "text": "are you there"}	DONE	1	\N	2026-07-29 07:58:07.703531
129	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTM2NTI1OTM5QTQxQjEzQUQxNDUxRjlEOEI2QUFGQwA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTM2NTI1OTM5QTQxQjEzQUQxNDUxRjlEOEI2QUFGQwA=", "user_id": "27672489700", "text": "hi"}	FAILED	3	(psycopg2.errors.UndefinedColumn) column "first_name" of relation "users" does not exist\nLINE 1: INSERT INTO users (id, first_name, last_name, display_name, ...\n                               ^\n\n[SQL: INSERT INTO users (id, first_name, last_name, display_	2026-07-30 02:32:05.44925
126	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUVBNkM5MkFEQ0NGQUU0RkFCMTU2MEFDRUFDNDYxRAA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUVBNkM5MkFEQ0NGQUU0RkFCMTU2MEFDRUFDNDYxRAA=", "user_id": "27672489700", "text": "hello"}	FAILED	3	(psycopg2.errors.UndefinedColumn) column "first_name" of relation "users" does not exist\nLINE 1: INSERT INTO users (id, first_name, last_name, display_name, ...\n                               ^\n\n[SQL: INSERT INTO users (id, first_name, last_name, display_	2026-07-30 02:30:16.38923
128	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTYxMTQ0NURCNTNBNTZCRTY0RDVCRUYxRkRBRjQ0QwA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTYxMTQ0NURCNTNBNTZCRTY0RDVCRUYxRkRBRjQ0QwA=", "user_id": "27672489700", "text": "hi"}	FAILED	3	(psycopg2.errors.UndefinedColumn) column "first_name" of relation "users" does not exist\nLINE 1: INSERT INTO users (id, first_name, last_name, display_name, ...\n                               ^\n\n[SQL: INSERT INTO users (id, first_name, last_name, display_	2026-07-30 02:32:02.378986
127	wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNThBRTA2NEVDMjVENzgwNUI4OTcyREM5QjIwODVEQwA=	27672489700	{"id": "wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNThBRTA2NEVDMjVENzgwNUI4OTcyREM5QjIwODVEQwA=", "user_id": "27672489700", "text": "are you there"}	FAILED	3	(psycopg2.errors.UndefinedColumn) column "first_name" of relation "users" does not exist\nLINE 1: INSERT INTO users (id, first_name, last_name, display_name, ...\n                               ^\n\n[SQL: INSERT INTO users (id, first_name, last_name, display_	2026-07-30 02:30:56.916367
\.


--
-- Data for Name: processed_messages; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.processed_messages (message_id) FROM stdin;
wamid.test123
ABGGFlA5Fpa
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMkExOURCRUFBOTI1M0ZGRUM4AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUY5QzhBQzM1MjkwMjREMkIxNzMzQTBFQUY4NTI0MQA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTkxMThEQUYzMUU2NjkzRUY1NUYzQUUzQzZCNENFQQA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUEwMzVFODNBQTA2MDJEODYwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTlEMDY1MEYyN0MyODJCQkY0AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzdFMUM3RDdDNEY2NTNDMzZFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjA1NTJEMjRDNzUwMzMzQkExAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzU1MzQ5M0FGQUU1RUVBQjk5AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjMwQkU5M0Q0RTQxOTE2RjE4AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTk3QzY5Rjk2N0VDQjc4REFGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTZDRkEzMzc4RjA3M0ZDREE2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjE1NDdCQjg3MzI2RTA4QTNFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODI3QUIzQkM4REUzMjlFRkZGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQUNDNUNEMTMxN0IzQjhCRkE0AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkFFOTFFOUVCOUM0NjU0NURDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTExQjY3MzNCNDM3ODlDNzM1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzNFMzQ3NzY1MjNFNzQ5RUQyAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjJERTg1N0I2Qjc4QzY2MTBCAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTcxMjI1QjRENjAxNEZGNTI0AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkNGREJFMUFDNDE5QTNBRjBGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNTg4MkJBQTAzMTU1M0ZGREY2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzk5Njg4RTZCRkE1RkI0RTQ2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTcxQzY5QUY1QUVDM0RDOTRFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjgwOEFCMkIyRjIzNTM0MjQ4AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwN0UyMzE5Mzc0MUM3N0I2MkE0AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjUzMkEzMUE2NDc2RENBNkI1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQ0M4Qjg5NzY0RDZERkU0QUZDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTU3QjE1MzkxOTg5NUY4RDQyAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzBCNUZBRjJERjcyRDQ4ODkzAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTFEMDcyODFGNDZFMzU2NTA1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOERGOEIxQkNENUMwMzYyRjdFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwREQ4N0EzNDRGMTVBNEU3NkZFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjFCRENBRDY5M0I4QTYwNEM3AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODE2ODNCMTY0NjBBNEQ4MzA1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjZCMDcwNjBFQjE2RjhENzZDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUYyNUYzNTBBRkEwMkVEMEE0AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjkxQzBBNTg2MjgwNzMzNzJCAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTUxREFERkE1MjYxODhFMUE2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDNCQkMzMzk2QUVFMzg0NDQ1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRTdDRkE4MDMxM0VCNzNBOTYzAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkY2NkQwRkQ1QzI5NTNBNkMzAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTBCNTgyQzQ0RjY1QjAxRDEwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUUwQkJCMzBERDYxNjVFMzM3AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTNGMEQ1MEMzMkQ4NEQ3OTlEAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNThEODI5NEQ5RTFGMDlDMEY1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUI1RUM5OTU0MDFERkM2MTI5AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODNCNEEyRTM1MjlDRDBCM0ZDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzVFRDM5RTRDMUQ5NEEzMUZDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjYwNDU1QjlDMjEyRDQ1MkMwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzQ2QUU2RENFNDYwQjEyQzNFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkU5MTBDMTk5NDVDRDgyNjRCAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTA4ODc1NzA0RjNDRUIxNEJBAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOEQyOURCMjVBQTExMDFCN0Y4AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjM1NjczMzEzRDc2QkIwQTMyAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMDg5RUU3NTAwMkM5OTY1RUQxAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUIwQTg1MkI1QjM5RTNENzM2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTMwNEQwOUEyQTlEQTQwRTk5AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMEYxRTUwNkNBOEU2QjZCN0FGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjgzODI2MjJGNjcyOTlDRDIwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjVDMDFGQ0EyMDEzMkNCODY3AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMDM4NTY5QUFDNDQ3NzBEQkE1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQzdDQzI4QzdDNTk3ODBBNjMzAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkM0OEJENDQzMzkwNjM0RDJBAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzAzNUY4MzRDMzEzOTQ0NzFCAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOTZGQkRCNzA3MzBEQTUwM0QxAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNDU0OTVBMkM4QjgxQzM4QkQ3AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTAxNTU5MTIwREVEMzE4OEMwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjdBQzhCQ0Y4QkJENDVEMTNGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwOEI2MzhGNzhFQTdBNERGOTJGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNTdGMDBBNTYzQUREMUI4RTlGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjZGOTlGNzIxNTQxQkVBM0ZGAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQUYxNjlCNUE5QjgwRTY5RUZFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjYzMTBFQzJBMEIzRjVGOUI4AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjZCRjYwRDA1MDVDMTM1RkNDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkI1MkExNzAwNDRGMzdEODJDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjFGNjI3RDZBNkQ4OTQ4MTI4AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzc5RjA1OUE4RUY1OUE0QjA2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNkVFNkJGNzU4MzY2QURGNThCAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTIzNDEwMDU3MDVFNTQ3RUYwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzIxODEwNzJGOTdCNUYyNDI0AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQTE3QTA1MjhEOUI4MTlFMDZBAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkQ3QUVDMjE3MzUwRkVEQzI2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwREEwRTJGNDNGMkVERjBCRTBFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODVEODEyNjZBODcxNkYzRTM1AA==
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzE2NUFGNDIzNTVCNkIxRDBDODVCMTk0NDQ1MzM3QQA=
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQ0ZGMjY0Rjk4MzRENDRBM0MzMUZFRDYyMkZENTgwNAA=
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzFBMTQ1NjBBNjg0NjlERDY3NUY0OTZCNjY5NEM2NQA=
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzhCMTBCMDEwNzI4ODAzMTJBMURCQUIxNTRCQjA3RgA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTk2QzNDNTZEQzVGMEEyOUZBOTJFRjUwNjRFQjM5OQA=
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzg5MEVFNEQyOEY1OENDMTA1Rjc3NDcyRTk2REQ1RAA=
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQ0MxMTY4REU0MDYyN0ZEQkY0N0FCMDJEM0YyOUY1RgA=
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzE0MDg0NzdENjk2QUIxMUYxNTMwOEZGN0JGQjVEOQA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNzQ3OEMwQ0QwMkQwQUU1RDFCAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDkwMjlDMDREMjQ2NzBCNzRBAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMkFCQzA3QTJENTc2MkI2RDcwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMjIwOTY2NkYzMzZFNjg3MjU3AA==
wamid.HBgLMjc3Mzg2NTE0MzkVAgASGCBBQzNEOTU3QTEwQTNBOEVFMDYwNjRFQzIyMkNFNzI3MQA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMzVGRTFGNEY2NUU4QkUwOTY2AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNEJENUMxNTFFNkQzM0RCMzYzAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRkJDNzMwN0FFNUZFRUMzRjU0AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMUIyM0YyNkZBNERCQkI2MkVDAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMEJFQThCNzY5QUU2RkI0QTYzAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQjFDQkQxOUI0RDIwMjgzRjZBAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjlGOUIwOTFFMzQ0Qzc2MUJEAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRDU0NUE1QjgxOUNGMkY1MDQ3AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNjA0NEI0OTgxNjMxQTYwN0M3AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRjE2MjU2MkUxODkzREVCMEFCAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwQkYwOEIzQjg5MzQxQjg2QzJBAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwODJDMDYxOUQ4M0U4QkM0Q0E1AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwM0JCNTc0N0QxNTgwNDdBOUI5AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwRUM1MEYzQzA5ODU3QTczRjQ5AA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNDgwNkE4MjM1QUE0M0RBQTAwAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwMTUwNUQwNjczRUNCRUMzNTZFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGBYzRUIwNkZDMjZCOTQyNTJDN0Q0NjZFAA==
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUI4QzBEMDREMkMyNDJBNTkzQUFBREQ2ODk2RDQ0NgA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTdCN0ZCMTlEMkUxODREOThDRkI2QjBDQzlDMzg3RgA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTc4MzM4MTY1MEQwQUU4MDM0MDlCNDkwOEM4RjExRAA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTQ0NTdEN0JCNjk3ODVBNjhBNEZEQTlEMjJCQzlCMQA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUVGQUFDNUM4NDE1OUIxN0I4NzE0REM0N0MwNDUwRAA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUJBODcxNDNBOUFENTlCOTdGNDM4RDUzOTE4NUU1RQA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTcwREVDRDI5OTg5NjY0QTNEMDFGRDQxMEJENkRBRAA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTNGQjhDMkQ1NUNGQjI2QTlCN0Q0MTU0QkY5MEM0MQA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUJGOTRGQjRFMjQ2MDkyNjI3MTRBRTBFRkM1QTU0QgA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNUVBNkM5MkFEQ0NGQUU0RkFCMTU2MEFDRUFDNDYxRAA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNThBRTA2NEVDMjVENzgwNUI4OTcyREM5QjIwODVEQwA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTYxMTQ0NURCNTNBNTZCRTY0RDVCRUYxRkRBRjQ0QwA=
wamid.HBgLMjc2NzI0ODk3MDAVAgASGCBBNTM2NTI1OTM5QTQxQjEzQUQxNDUxRjlEOEI2QUFGQwA=
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.transactions (id, user_id, amount, status, idempotency_key) FROM stdin;
77ef8260-3a6a-4dd1-8b4e-a01d352054e1	27672489700	1000	PENDING	\N
6c87cfbc-8c83-47d4-a883-c8f930418f93	27672489700	1000	PENDING	\N
72e18005-b886-4473-a274-a816a81504c8	27672489700	1000	PENDING	\N
b93ce77c-c68b-4dc3-b52b-16d5262757ad	27672489700	1000	PENDING	\N
4f21517d-22a6-4548-a379-b600cdbf6199	27672489700	1000	PENDING	\N
f72e85bc-8da2-42f4-99f5-8155573611ae	27672489700	200	PENDING	\N
4ff416af-14ef-403d-a8a9-75ddfd10a636	27672489700	2000	PENDING	\N
\.


--
-- Data for Name: user_identities; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.user_identities (id, user_id, provider, provider_identifier, verified, created_at) FROM stdin;
\.


--
-- Data for Name: user_sessions; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.user_sessions (user_id, state, context, last_seen, expires_at) FROM stdin;
16315551181	\N	{}	\N	\N
27672489700	\N	{}	\N	\N
27738651439	\N	{"flow": "contribution", "step": "awaiting_amount"}	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: warima_user
--

COPY public.users (id, user_id, user_name, status, balance, message_id) FROM stdin;
\.


--
-- Name: conversation_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: warima_user
--

SELECT pg_catalog.setval('public.conversation_messages_id_seq', 244, true);


--
-- Name: event_queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: warima_user
--

SELECT pg_catalog.setval('public.event_queue_id_seq', 129, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: conversation_messages conversation_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.conversation_messages
    ADD CONSTRAINT conversation_messages_pkey PRIMARY KEY (id);


--
-- Name: event_queue event_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.event_queue
    ADD CONSTRAINT event_queue_pkey PRIMARY KEY (id);


--
-- Name: processed_messages processed_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.processed_messages
    ADD CONSTRAINT processed_messages_pkey PRIMARY KEY (message_id);


--
-- Name: transactions transactions_idempotency_key_key; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_idempotency_key_key UNIQUE (idempotency_key);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: user_identities uq_provider_identifier; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.user_identities
    ADD CONSTRAINT uq_provider_identifier UNIQUE (provider, provider_identifier);


--
-- Name: user_identities user_identities_pkey; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.user_identities
    ADD CONSTRAINT user_identities_pkey PRIMARY KEY (id);


--
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_conversation_messages_user_id; Type: INDEX; Schema: public; Owner: warima_user
--

CREATE INDEX ix_conversation_messages_user_id ON public.conversation_messages USING btree (user_id);


--
-- Name: ix_event_queue_id; Type: INDEX; Schema: public; Owner: warima_user
--

CREATE INDEX ix_event_queue_id ON public.event_queue USING btree (id);


--
-- Name: ix_event_queue_message_id; Type: INDEX; Schema: public; Owner: warima_user
--

CREATE UNIQUE INDEX ix_event_queue_message_id ON public.event_queue USING btree (message_id);


--
-- Name: ix_event_queue_user_id; Type: INDEX; Schema: public; Owner: warima_user
--

CREATE INDEX ix_event_queue_user_id ON public.event_queue USING btree (user_id);


--
-- Name: ix_provider_identifier; Type: INDEX; Schema: public; Owner: warima_user
--

CREATE INDEX ix_provider_identifier ON public.user_identities USING btree (provider, provider_identifier);


--
-- Name: user_identities user_identities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: warima_user
--

ALTER TABLE ONLY public.user_identities
    ADD CONSTRAINT user_identities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 5vxhrpwfuBruim8DDHJynm1WPpnaF9BzpgF4Sra9j8yLQI4HQZMwLgTMo0AaHd3

