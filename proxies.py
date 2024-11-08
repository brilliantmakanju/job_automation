import re


# The raw proxy data as a string
proxy_data = """
IP Address	Port	Code	Country	Anonymity	Google	Https	Last Checked
47.251.70.179	80	US	United States	elite proxy	no	yes	24 secs ago
20.44.189.184	3129	JP	Japan	anonymous	no	yes	24 secs ago
20.44.188.17	3129	JP	Japan	anonymous	no	yes	24 secs ago
20.219.176.57	3129	IN	India	anonymous	no	yes	24 secs ago
189.240.60.166	9090	MX	Mexico	elite proxy	no	yes	20 mins ago
184.168.124.233	5402	SG	Singapore	elite proxy	no	yes	20 mins ago
189.240.60.164	9090	MX	Mexico	elite proxy	no	yes	20 mins ago
189.240.60.168	9090	MX	Mexico	elite proxy	no	yes	20 mins ago
5.45.107.19	3128	DE	Germany	anonymous	no	yes	20 mins ago
47.243.166.133	18080	HK	Hong Kong	anonymous		yes	30 mins ago
47.251.43.115	33333	US	United States	anonymous		yes	30 mins ago
200.174.198.86	8888	BR	Brazil	anonymous	no	yes	30 mins ago
172.183.241.1	8080	US	United States	elite proxy	no	yes	40 mins ago
20.204.212.76	3129	IN	India	anonymous	no	yes	50 mins ago
189.240.60.163	9090	MX	Mexico	elite proxy	no	yes	50 mins ago
212.92.148.164	8090	RU	Russian Federation	elite proxy	no	yes	50 mins ago
103.237.144.232	1311	VN	Vietnam	elite proxy	no	yes	50 mins ago
160.86.242.23	8080	JP	Japan	elite proxy	no	yes	50 mins ago
20.204.214.23	3129	IN	India	anonymous	yes	yes	50 mins ago
20.204.212.45	3129	IN	India	anonymous	no	yes	50 mins ago
47.88.31.196	8080	US	United States	anonymous	no	yes	50 mins ago
218.76.247.34	30000	CN	China	anonymous		yes	1 hour ago
8.223.31.16	80	SG	Singapore	anonymous	yes	yes	1 hour 1 min ago
20.235.159.154	80	IN	India	anonymous	no	yes	1 hour 1 min ago
35.185.196.38	3128	US	United States	anonymous	yes	yes	1 hour 1 min ago
51.8.224.206	9000	US	United States	elite proxy	no	yes	1 hour 1 min ago
212.92.148.162	8090	RU	Russian Federation	elite proxy	no	yes	1 hour 1 min ago
72.10.160.172	9739	CA	Canada	elite proxy	no	yes	1 hour 10 mins ago
72.10.160.90	1365	CA	Canada	elite proxy	no	yes	1 hour 10 mins ago
148.72.165.7	30135	US	United States	anonymous		yes	1 hour 10 mins ago
67.43.236.18	1853	CA	Canada	anonymous		yes	1 hour 10 mins ago
8.219.97.248	80	SG	Singapore	anonymous	no	yes	1 hour 10 mins ago
148.72.140.24	30127	US	United States	elite proxy	yes	yes	1 hour 10 mins ago
114.129.2.82	8081	JP	Japan	elite proxy	no	yes	1 hour 20 mins ago
72.10.160.91	8167	CA	Canada	elite proxy	yes	yes	1 hour 20 mins ago
67.43.236.20	10145	CA	Canada	elite proxy	no	yes	1 hour 40 mins ago
189.240.60.171	9090	MX	Mexico	elite proxy	no	yes	1 hour 40 mins ago
67.43.227.227	11023	CA	Canada	elite proxy	yes	yes	1 hour 50 mins ago
223.135.156.183	8080	JP	Japan	elite proxy	no	yes	1 hour 50 mins ago
67.43.236.21	8307	CA	Canada	elite proxy	yes	yes	1 hour 50 mins ago
5.189.184.6	80	DE	Germany	elite proxy	no	yes	2 hours 30 mins ago
47.90.205.231	33333	US	United States	anonymous	no	yes	2 hours 50 mins ago
67.43.228.253	12915	CA	Canada	elite proxy	yes	yes	3 hours 40 mins ago
47.245.120.95	8080	SG	Singapore	anonymous	no	yes	4 hours 20 mins ago
149.11.58.226	3128	FR	France	anonymous	no	yes	4 hours 30 mins ago
171.244.60.55	8080	VN	Vietnam	anonymous	no	yes	4 hours 30 mins ago
67.43.228.250	26991	CA	Canada	elite proxy	yes	yes	4 hours 40 mins ago
213.230.71.175	3128	UZ	Uzbekistan	elite proxy	no	yes	4 hours 40 mins ago
67.43.236.22	28607	CA	Canada	elite proxy	yes	yes	4 hours 51 mins ago
43.132.124.11	3128	HK	Hong Kong	anonymous	no	yes	5 hours 10 mins ago
154.236.177.100	1976	EG	Egypt	elite proxy		yes	5 hours 21 mins ago
107.172.209.246	9090	US	United States	elite proxy	no	yes	5 hours 40 mins ago
54.207.238.99	8888	BR	Brazil	elite proxy	no	yes	6 hours 40 mins ago
72.10.160.94	18345	CA	Canada	elite proxy	yes	yes	7 hours ago
67.43.228.254	2679	CA	Canada	elite proxy	yes	yes	7 hours 10 mins ago
51.210.255.127	80	FR	France	anonymous	yes	yes	7 hours 20 mins ago
67.43.228.252	10579	CA	Canada	elite proxy	yes	yes	7 hours 31 mins ago
24.207.79.154	8000	CA	Canada	anonymous	yes	yes	7 hours 31 mins ago
185.25.204.192	8080	IT	Italy	anonymous	no	yes	7 hours 31 mins ago
64.206.77.122	3128	US	United States	anonymous	no	yes	7 hours 41 mins ago
41.173.7.82	8080	UG	Uganda	anonymous	no	yes	7 hours 41 mins ago
45.77.147.46	3128	US	United States	anonymous	no	yes	8 hours ago
20.27.86.185	8080	JP	Japan	anonymous	yes	yes	8 hours 11 mins ago
156.240.111.19	59145	HK	Hong Kong	anonymous	yes	yes	8 hours 11 mins ago
67.43.227.228	23737	CA	Canada	elite proxy	yes	yes	8 hours 20 mins ago
95.154.20.113	34248	DK	Denmark	anonymous		yes	8 hours 40 mins ago
46.246.14.4	8118	SE	Sweden	elite proxy	no	yes	8 hours 40 mins ago
34.124.190.108	8090	SG	Singapore	anonymous	no	yes	8 hours 51 mins ago
"""

# Regular expression to match proxy entries with HTTPS support
proxy_regex = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+\S+\s+.*\s+yes\s+\d+\s+\w+\s+ago", re.MULTILINE)

# Find all proxies matching the regex
https_proxies = proxy_regex.findall(proxy_data)

# Format the proxies as a list of proxy strings
https_proxies_list = [f"{ip}:{port}" for ip, port in https_proxies]

# Print the extracted HTTPS proxies
for proxy in https_proxies_list:
    print(f'"{proxy}",')
