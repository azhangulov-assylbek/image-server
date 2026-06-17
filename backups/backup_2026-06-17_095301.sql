--
-- PostgreSQL database dump
--

\restrict JoV3eyKgUN3Cmh5wGTvqpg12XY0pnPaAP1vm8RAM5oGtZ7x3o8UjdrpHDlpRKyh

-- Dumped from database version 15.18 (Debian 15.18-1.pgdg13+1)
-- Dumped by pg_dump version 15.18 (Debian 15.18-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    id integer NOT NULL,
    filename character varying(100) NOT NULL,
    original_name character varying(100) NOT NULL,
    size integer NOT NULL,
    upload_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    file_type character varying(10) NOT NULL
);


ALTER TABLE public.images OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_id_seq OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (id, filename, original_name, size, upload_date, file_type) FROM stdin;
1	ac8328240d234436b742df22137c3564.jpg	photo.jpg	216290	2026-06-16 09:20:26.30458	.jpg
2	5f5186eda742420ea5ee99b6981d8c9b.jpg	photo29.jpg	132221	2026-06-16 09:20:58.762521	.jpg
3	826beeccd04f4efeaf760d8577ed4033.png	IMG_0309.PNG	5117672	2026-06-16 09:21:07.857975	.png
4	01a3b5d001db49e4a1078bee9eb30290.jpg	photo29.jpg	132221	2026-06-16 09:35:52.297537	.jpg
5	8f78a29b268d48b5a457d7917ca70919.jpg	photo29.jpg	132221	2026-06-16 14:31:29.182453	.jpg
6	3013fb8d806c45c1835b3fe20e9fc9fd.jpg	photo.jpg	216290	2026-06-16 17:29:06.528565	.jpg
7	5ffa661d18ac4ca5851908b93e9f0b61.jpg	photo29.jpg	132221	2026-06-16 17:45:40.713792	.jpg
8	25c7434ffd54400a93a85a573c22264a.jpg	photo.jpg	216290	2026-06-16 17:45:40.851452	.jpg
9	ebca96d4bb904342a5955c1ed2720cf0.jpg	photo29.jpg	132221	2026-06-16 17:45:50.033183	.jpg
10	8bba5727556a426fb2bb9156236704e3.jpg	photo.jpg	216290	2026-06-16 17:45:50.125306	.jpg
11	3cb7da60ba9d4ce79b5f76d2c448c0b2.jpg	photo_2026-05-27_23-52-41.jpg	99590	2026-06-16 17:49:22.458911	.jpg
13	76f8cf4f286e48dab4eb190401bd4545.jpg	photo_2026-06-01_11-43-26.jpg	113006	2026-06-16 17:49:22.659326	.jpg
14	2ed6abff3c87470699c195267d2e9d9b.jpg	photo_2026-06-02_16-30-23.jpg	63330	2026-06-16 17:49:22.750133	.jpg
16	9e3c1c07a30348a39c2766b6779cb307.jpg	photo_2026-06-05_12-30-43 (2).jpg	94239	2026-06-16 17:49:22.892297	.jpg
18	1ee171cfb35c4f09bf4edef695f05a05.jpg	photo_2026-06-05_12-30-43.jpg	67436	2026-06-16 17:49:23.018621	.jpg
19	d25360f9a46d49c3bdc9994a29bf60bb.jpg	photo_2026-06-05_12-30-42.jpg	51048	2026-06-16 17:49:23.05372	.jpg
20	6c38d87c323e48dc9991f22f5f6285be.jpg	photo_2026-06-07_01-25-27.jpg	50362	2026-06-16 17:49:23.163059	.jpg
21	e5227ddd8b624b0aa5ad5b0e7f27e966.jpg	photo_2026-06-12_12-20-34.jpg	85950	2026-06-16 17:49:23.25903	.jpg
22	abcaa265f1224ce7a3f011388e52344b.jpg	photo_2026-06-05_12-30-43.jpg	67436	2026-06-16 19:00:49.356997	.jpg
23	3f79ca9cd99548e79fa298358f80fcae.jpg	photo_2026-06-05_12-30-43 (2).jpg	94239	2026-06-17 02:41:26.227081	.jpg
\.


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.images_id_seq', 23, true);


--
-- Name: images images_filename_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_filename_key UNIQUE (filename);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict JoV3eyKgUN3Cmh5wGTvqpg12XY0pnPaAP1vm8RAM5oGtZ7x3o8UjdrpHDlpRKyh

