--
-- PostgreSQL database dump
--

\restrict 27CQ3OFi9DiJrfMXB1KIiNeZH9ijTK2ygyckz3LWNZYPNR1NIhfOIuBcsXrHPLc

-- Dumped from database version 17.6 (Homebrew)
-- Dumped by pg_dump version 17.6 (Homebrew)

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
-- Name: requestconditions; Type: TYPE; Schema: public; Owner: fastapi
--

CREATE TYPE public.requestconditions AS ENUM (
    'PENDING',
    'CONFIRMED',
    'REJECTED'
);


ALTER TYPE public.requestconditions OWNER TO fastapi;

--
-- Name: tenanttypes; Type: TYPE; Schema: public; Owner: fastapi
--

CREATE TYPE public.tenanttypes AS ENUM (
    'IMB_EDU',
    'IMB_HR'
);


ALTER TYPE public.tenanttypes OWNER TO fastapi;

--
-- Name: userroles; Type: TYPE; Schema: public; Owner: fastapi
--

CREATE TYPE public.userroles AS ENUM (
    'admin',
    'seller',
    'super_admin'
);


ALTER TYPE public.userroles OWNER TO fastapi;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO fastapi;

--
-- Name: seller_requests; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.seller_requests (
    seller_id integer NOT NULL,
    amount numeric(36,2) DEFAULT '0'::numeric NOT NULL,
    date date NOT NULL,
    condition public.requestconditions NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.seller_requests OWNER TO fastapi;

--
-- Name: COLUMN seller_requests.amount; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.seller_requests.amount IS 'The amount of the seller request';


--
-- Name: COLUMN seller_requests.date; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.seller_requests.date IS 'The date of the seller request';


--
-- Name: COLUMN seller_requests.condition; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.seller_requests.condition IS 'The condition of the seller request';


--
-- Name: seller_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi
--

CREATE SEQUENCE public.seller_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seller_requests_id_seq OWNER TO fastapi;

--
-- Name: seller_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi
--

ALTER SEQUENCE public.seller_requests_id_seq OWNED BY public.seller_requests.id;


--
-- Name: supervisors; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.supervisors (
    supervisor_id integer NOT NULL,
    seller_id integer NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    percentage numeric(5,2) NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.supervisors OWNER TO fastapi;

--
-- Name: COLUMN supervisors.from_date; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.supervisors.from_date IS 'The start date of the assistants deadline';


--
-- Name: COLUMN supervisors.to_date; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.supervisors.to_date IS 'The end date of the assistants deadline';


--
-- Name: COLUMN supervisors.percentage; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.supervisors.percentage IS 'The percentage of the assistants deadline';


--
-- Name: supervisors_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi
--

CREATE SEQUENCE public.supervisors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.supervisors_id_seq OWNER TO fastapi;

--
-- Name: supervisors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi
--

ALTER SEQUENCE public.supervisors_id_seq OWNED BY public.supervisors.id;


--
-- Name: tenant_monthly_transactions; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.tenant_monthly_transactions (
    tenant_id integer NOT NULL,
    service_id integer NOT NULL,
    month date NOT NULL,
    amount numeric(36,2) DEFAULT 0.00 NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tenant_monthly_transactions OWNER TO fastapi;

--
-- Name: COLUMN tenant_monthly_transactions.service_id; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_monthly_transactions.service_id IS 'Core service, MonthlyTransaction ID';


--
-- Name: COLUMN tenant_monthly_transactions.month; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_monthly_transactions.month IS 'Month: format YEAR-MONTH-01';


--
-- Name: COLUMN tenant_monthly_transactions.amount; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_monthly_transactions.amount IS 'Month: amount of monthly transaction';


--
-- Name: tenant_monthly_transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi
--

CREATE SEQUENCE public.tenant_monthly_transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tenant_monthly_transactions_id_seq OWNER TO fastapi;

--
-- Name: tenant_monthly_transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi
--

ALTER SEQUENCE public.tenant_monthly_transactions_id_seq OWNED BY public.tenant_monthly_transactions.id;


--
-- Name: tenant_tg_chat; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.tenant_tg_chat (
    name character varying NOT NULL,
    chat_id bigint NOT NULL,
    message_thread_id integer DEFAULT 0 NOT NULL,
    is_active boolean NOT NULL,
    core_tenant_id integer NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tenant_tg_chat OWNER TO fastapi;

--
-- Name: COLUMN tenant_tg_chat.name; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_tg_chat.name IS 'Telegram chat name';


--
-- Name: COLUMN tenant_tg_chat.chat_id; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_tg_chat.chat_id IS 'Telegram chat id';


--
-- Name: COLUMN tenant_tg_chat.message_thread_id; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_tg_chat.message_thread_id IS 'Super chats topic id';


--
-- Name: COLUMN tenant_tg_chat.is_active; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_tg_chat.is_active IS 'Is active?';


--
-- Name: COLUMN tenant_tg_chat.core_tenant_id; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenant_tg_chat.core_tenant_id IS 'Core service client id';


--
-- Name: tenant_tg_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi
--

CREATE SEQUENCE public.tenant_tg_chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tenant_tg_chat_id_seq OWNER TO fastapi;

--
-- Name: tenant_tg_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi
--

ALTER SEQUENCE public.tenant_tg_chat_id_seq OWNED BY public.tenant_tg_chat.id;


--
-- Name: tenants; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.tenants (
    core_tenant_id integer NOT NULL,
    type public.tenanttypes NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    percentage numeric(5,2) NOT NULL,
    seller_id integer,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tenants OWNER TO fastapi;

--
-- Name: COLUMN tenants.core_tenant_id; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenants.core_tenant_id IS 'Tenant id: in core service!';


--
-- Name: COLUMN tenants.type; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenants.type IS 'The type of the tenant';


--
-- Name: COLUMN tenants.from_date; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenants.from_date IS 'The start date of the tenant';


--
-- Name: COLUMN tenants.to_date; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenants.to_date IS 'The end date of the tenant';


--
-- Name: COLUMN tenants.percentage; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tenants.percentage IS 'The percentage of the tenant';


--
-- Name: tenants_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi
--

CREATE SEQUENCE public.tenants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tenants_id_seq OWNER TO fastapi;

--
-- Name: tenants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi
--

ALTER SEQUENCE public.tenants_id_seq OWNED BY public.tenants.id;


--
-- Name: tg_chat_message_history; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.tg_chat_message_history (
    chat_id integer NOT NULL,
    sender_id integer NOT NULL,
    message character varying(555) NOT NULL,
    is_delivered boolean NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    tg_response json
);


ALTER TABLE public.tg_chat_message_history OWNER TO fastapi;

--
-- Name: COLUMN tg_chat_message_history.message; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tg_chat_message_history.message IS 'Sent message body';


--
-- Name: COLUMN tg_chat_message_history.is_delivered; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tg_chat_message_history.is_delivered IS 'Is delivered?';


--
-- Name: COLUMN tg_chat_message_history.tg_response; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.tg_chat_message_history.tg_response IS 'Telegram API response payload';


--
-- Name: tg_chat_message_history_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi
--

CREATE SEQUENCE public.tg_chat_message_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tg_chat_message_history_id_seq OWNER TO fastapi;

--
-- Name: tg_chat_message_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi
--

ALTER SEQUENCE public.tg_chat_message_history_id_seq OWNED BY public.tg_chat_message_history.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: fastapi
--

CREATE TABLE public.users (
    username character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    phone character varying(255),
    role public.userroles DEFAULT 'seller'::public.userroles NOT NULL,
    is_active boolean NOT NULL,
    percentage numeric(5,2) NOT NULL,
    duration integer NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO fastapi;

--
-- Name: COLUMN users.username; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.username IS 'Username';


--
-- Name: COLUMN users.full_name; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.full_name IS 'User''s full name';


--
-- Name: COLUMN users.password; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.password IS 'User''s password';


--
-- Name: COLUMN users.phone; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.phone IS 'User''s phone number';


--
-- Name: COLUMN users.role; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.role IS 'User''s role';


--
-- Name: COLUMN users.is_active; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.is_active IS 'Whether the user is active';


--
-- Name: COLUMN users.percentage; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.percentage IS 'User''s percentage';


--
-- Name: COLUMN users.duration; Type: COMMENT; Schema: public; Owner: fastapi
--

COMMENT ON COLUMN public.users.duration IS 'The duration of the user';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO fastapi;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: seller_requests id; Type: DEFAULT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.seller_requests ALTER COLUMN id SET DEFAULT nextval('public.seller_requests_id_seq'::regclass);


--
-- Name: supervisors id; Type: DEFAULT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.supervisors ALTER COLUMN id SET DEFAULT nextval('public.supervisors_id_seq'::regclass);


--
-- Name: tenant_monthly_transactions id; Type: DEFAULT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenant_monthly_transactions ALTER COLUMN id SET DEFAULT nextval('public.tenant_monthly_transactions_id_seq'::regclass);


--
-- Name: tenant_tg_chat id; Type: DEFAULT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenant_tg_chat ALTER COLUMN id SET DEFAULT nextval('public.tenant_tg_chat_id_seq'::regclass);


--
-- Name: tenants id; Type: DEFAULT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenants ALTER COLUMN id SET DEFAULT nextval('public.tenants_id_seq'::regclass);


--
-- Name: tg_chat_message_history id; Type: DEFAULT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tg_chat_message_history ALTER COLUMN id SET DEFAULT nextval('public.tg_chat_message_history_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.alembic_version (version_num) FROM stdin;
f9dccb8c6b28
\.


--
-- Data for Name: seller_requests; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.seller_requests (seller_id, amount, date, condition, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: supervisors; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.supervisors (supervisor_id, seller_id, from_date, to_date, percentage, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: tenant_monthly_transactions; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.tenant_monthly_transactions (tenant_id, service_id, month, amount, id, created_at, updated_at) FROM stdin;
4	0	2026-05-18	0.00	1	2026-05-18 11:24:18.740428+05	2026-05-18 11:24:18.740428+05
\.


--
-- Data for Name: tenant_tg_chat; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.tenant_tg_chat (name, chat_id, message_thread_id, is_active, core_tenant_id, id, created_at, updated_at) FROM stdin;
Tenant-101 Chat	-1001000000101	0	t	101	1	2026-05-18 10:31:35.236508+05	2026-05-18 10:31:35.236508+05
Tenant-102 Chat	-1001000000102	0	t	102	2	2026-05-18 10:31:35.236508+05	2026-05-18 10:31:35.236508+05
Tenant-103 Chat	-1001000000103	0	t	103	3	2026-05-18 10:31:35.236508+05	2026-05-18 10:31:35.236508+05
\.


--
-- Data for Name: tenants; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.tenants (core_tenant_id, type, from_date, to_date, percentage, seller_id, id, created_at, updated_at) FROM stdin;
101	IMB_HR	2024-01-01	2025-01-01	10.00	1	1	2026-05-18 10:31:30.035558+05	2026-05-18 10:31:30.035558+05
102	IMB_HR	2024-03-01	2025-03-01	15.00	1	2	2026-05-18 10:31:30.035558+05	2026-05-18 10:31:30.035558+05
103	IMB_HR	2024-06-01	2025-06-01	12.50	1	3	2026-05-18 10:31:30.035558+05	2026-05-18 10:31:30.035558+05
92	IMB_HR	2026-05-18	2026-05-18	0.00	1	4	2026-05-18 11:10:56.998365+05	2026-05-18 11:10:56.998365+05
91	IMB_HR	2026-05-18	2026-05-18	0.00	\N	6	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
90	IMB_HR	2026-05-18	2026-05-18	0.00	\N	7	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
89	IMB_HR	2026-05-18	2026-05-18	0.00	\N	8	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
88	IMB_HR	2026-05-18	2026-05-18	0.00	\N	9	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
87	IMB_HR	2026-05-18	2026-05-18	0.00	\N	10	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
86	IMB_HR	2026-05-18	2026-05-18	0.00	\N	11	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
85	IMB_HR	2026-05-18	2026-05-18	0.00	\N	12	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
84	IMB_HR	2026-05-18	2026-05-18	0.00	\N	13	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
83	IMB_HR	2026-05-18	2026-05-18	0.00	\N	14	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
82	IMB_HR	2026-05-18	2026-05-18	0.00	\N	15	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
81	IMB_HR	2026-05-18	2026-05-18	0.00	\N	16	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
80	IMB_HR	2026-05-18	2026-05-18	0.00	\N	17	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
79	IMB_HR	2026-05-18	2026-05-18	0.00	\N	18	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
78	IMB_HR	2026-05-18	2026-05-18	0.00	\N	19	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
77	IMB_HR	2026-05-18	2026-05-18	0.00	\N	20	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
76	IMB_HR	2026-05-18	2026-05-18	0.00	\N	21	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
75	IMB_HR	2026-05-18	2026-05-18	0.00	\N	22	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
74	IMB_HR	2026-05-18	2026-05-18	0.00	\N	23	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
73	IMB_HR	2026-05-18	2026-05-18	0.00	\N	24	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
72	IMB_HR	2026-05-18	2026-05-18	0.00	\N	25	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
71	IMB_HR	2026-05-18	2026-05-18	0.00	\N	26	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
70	IMB_HR	2026-05-18	2026-05-18	0.00	\N	27	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
69	IMB_HR	2026-05-18	2026-05-18	0.00	\N	28	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
68	IMB_HR	2026-05-18	2026-05-18	0.00	\N	29	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
67	IMB_HR	2026-05-18	2026-05-18	0.00	\N	30	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
62	IMB_HR	2026-05-18	2026-05-18	0.00	\N	31	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
61	IMB_HR	2026-05-18	2026-05-18	0.00	\N	32	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
60	IMB_HR	2026-05-18	2026-05-18	0.00	\N	33	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
59	IMB_HR	2026-05-18	2026-05-18	0.00	\N	34	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
58	IMB_HR	2026-05-18	2026-05-18	0.00	\N	35	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
57	IMB_HR	2026-05-18	2026-05-18	0.00	\N	36	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
56	IMB_HR	2026-05-18	2026-05-18	0.00	\N	37	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
52	IMB_HR	2026-05-18	2026-05-18	0.00	\N	38	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
51	IMB_HR	2026-05-18	2026-05-18	0.00	\N	39	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
50	IMB_HR	2026-05-18	2026-05-18	0.00	\N	40	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
49	IMB_HR	2026-05-18	2026-05-18	0.00	\N	41	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
48	IMB_HR	2026-05-18	2026-05-18	0.00	\N	42	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
47	IMB_HR	2026-05-18	2026-05-18	0.00	\N	43	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
46	IMB_HR	2026-05-18	2026-05-18	0.00	\N	44	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
45	IMB_HR	2026-05-18	2026-05-18	0.00	\N	45	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
43	IMB_HR	2026-05-18	2026-05-18	0.00	\N	46	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
36	IMB_HR	2026-05-18	2026-05-18	0.00	\N	47	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
35	IMB_HR	2026-05-18	2026-05-18	0.00	\N	48	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
33	IMB_HR	2026-05-18	2026-05-18	0.00	\N	49	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
26	IMB_HR	2026-05-18	2026-05-18	0.00	\N	50	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
25	IMB_HR	2026-05-18	2026-05-18	0.00	\N	51	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
23	IMB_HR	2026-05-18	2026-05-18	0.00	\N	52	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
22	IMB_HR	2026-05-18	2026-05-18	0.00	\N	53	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
19	IMB_HR	2026-05-18	2026-05-18	0.00	\N	54	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
18	IMB_HR	2026-05-18	2026-05-18	0.00	\N	55	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
13	IMB_HR	2026-05-18	2026-05-18	0.00	\N	56	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
11	IMB_HR	2026-05-18	2026-05-18	0.00	\N	57	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
7	IMB_HR	2026-05-18	2026-05-18	0.00	\N	58	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
6	IMB_HR	2026-05-18	2026-05-18	0.00	\N	59	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
1	IMB_HR	2026-05-18	2026-05-18	0.00	\N	60	2026-05-18 11:31:24.302737+05	2026-05-18 11:31:24.302737+05
\.


--
-- Data for Name: tg_chat_message_history; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.tg_chat_message_history (chat_id, sender_id, message, is_delivered, id, created_at, updated_at, tg_response) FROM stdin;
1	1	Tenant 101 uchun boshlang'ich xabar.	t	1	2026-05-18 10:31:35.236508+05	2026-05-18 10:31:35.236508+05	\N
2	1	Tenant 102 uchun boshlang'ich xabar.	t	2	2026-05-18 10:31:35.236508+05	2026-05-18 10:31:35.236508+05	\N
3	1	Tenant 103 uchun boshlang'ich xabar.	t	3	2026-05-18 10:31:35.236508+05	2026-05-18 10:31:35.236508+05	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: fastapi
--

COPY public.users (username, full_name, password, phone, role, is_active, percentage, duration, id, created_at, updated_at) FROM stdin;
seller	Seller User	$argon2id$v=19$m=65536,t=3,p=4$25vz3nuvdQ4hZEzpXYvR2g$qbcud4C9XnAL3HD3f1gtd8c3LkXxGyALIA/SkHKtZWs	\N	seller	t	0.00	0	1	2026-05-16 17:05:01.048215+05	2026-05-16 17:05:01.048215+05
admin	Admin User	$argon2id$v=19$m=65536,t=3,p=4$w5jzPgdAaM0ZQ8jZW4tx7g$xCm/uDbLfTZ+FB1hicJrBGOhtUrG83IoYP+5vvm7UA0	\N	admin	t	0.00	0	2	2026-05-16 17:05:07.581142+05	2026-05-16 17:05:07.581142+05
\.


--
-- Name: seller_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi
--

SELECT pg_catalog.setval('public.seller_requests_id_seq', 1, false);


--
-- Name: supervisors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi
--

SELECT pg_catalog.setval('public.supervisors_id_seq', 1, false);


--
-- Name: tenant_monthly_transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi
--

SELECT pg_catalog.setval('public.tenant_monthly_transactions_id_seq', 1, true);


--
-- Name: tenant_tg_chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi
--

SELECT pg_catalog.setval('public.tenant_tg_chat_id_seq', 3, true);


--
-- Name: tenants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi
--

SELECT pg_catalog.setval('public.tenants_id_seq', 60, true);


--
-- Name: tg_chat_message_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi
--

SELECT pg_catalog.setval('public.tg_chat_message_history_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: seller_requests seller_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.seller_requests
    ADD CONSTRAINT seller_requests_pkey PRIMARY KEY (id);


--
-- Name: supervisors supervisors_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.supervisors
    ADD CONSTRAINT supervisors_pkey PRIMARY KEY (id);


--
-- Name: tenant_monthly_transactions tenant_monthly_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenant_monthly_transactions
    ADD CONSTRAINT tenant_monthly_transactions_pkey PRIMARY KEY (id);


--
-- Name: tenant_tg_chat tenant_tg_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenant_tg_chat
    ADD CONSTRAINT tenant_tg_chat_pkey PRIMARY KEY (id);


--
-- Name: tenants tenants_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_pkey PRIMARY KEY (id);


--
-- Name: tg_chat_message_history tg_chat_message_history_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tg_chat_message_history
    ADD CONSTRAINT tg_chat_message_history_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_seller_requests_id; Type: INDEX; Schema: public; Owner: fastapi
--

CREATE INDEX ix_seller_requests_id ON public.seller_requests USING btree (id);


--
-- Name: ix_supervisors_id; Type: INDEX; Schema: public; Owner: fastapi
--

CREATE INDEX ix_supervisors_id ON public.supervisors USING btree (id);


--
-- Name: ix_tenant_monthly_transactions_id; Type: INDEX; Schema: public; Owner: fastapi
--

CREATE INDEX ix_tenant_monthly_transactions_id ON public.tenant_monthly_transactions USING btree (id);


--
-- Name: ix_tenant_tg_chat_id; Type: INDEX; Schema: public; Owner: fastapi
--

CREATE INDEX ix_tenant_tg_chat_id ON public.tenant_tg_chat USING btree (id);


--
-- Name: ix_tenants_id; Type: INDEX; Schema: public; Owner: fastapi
--

CREATE INDEX ix_tenants_id ON public.tenants USING btree (id);


--
-- Name: ix_tg_chat_message_history_id; Type: INDEX; Schema: public; Owner: fastapi
--

CREATE INDEX ix_tg_chat_message_history_id ON public.tg_chat_message_history USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: fastapi
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: seller_requests seller_requests_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.seller_requests
    ADD CONSTRAINT seller_requests_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: supervisors supervisors_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.supervisors
    ADD CONSTRAINT supervisors_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: supervisors supervisors_supervisor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.supervisors
    ADD CONSTRAINT supervisors_supervisor_id_fkey FOREIGN KEY (supervisor_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: tenant_monthly_transactions tenant_monthly_transactions_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenant_monthly_transactions
    ADD CONSTRAINT tenant_monthly_transactions_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: tenants tenants_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: tg_chat_message_history tg_chat_message_history_chat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tg_chat_message_history
    ADD CONSTRAINT tg_chat_message_history_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES public.tenant_tg_chat(id) ON DELETE CASCADE;


--
-- Name: tg_chat_message_history tg_chat_message_history_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi
--

ALTER TABLE ONLY public.tg_chat_message_history
    ADD CONSTRAINT tg_chat_message_history_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 27CQ3OFi9DiJrfMXB1KIiNeZH9ijTK2ygyckz3LWNZYPNR1NIhfOIuBcsXrHPLc

