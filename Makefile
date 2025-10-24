proxy:
	clear && python3 python_tcp_server/proxy/proxy.py

client:
	clear && python3 python_tcp_server/client/client.py

agent:
	clear && python3 python_tcp_server/agent/agent.py

kill-ports:
    kill -9 $(lsof -t -i:50050)
    kill -9 $(lsof -t -i:50051)
	@{ \
		pids=$$(lsof -t -i:50050 -i:50051 2>/dev/null); \
		if [ -n "$$pids" ]; then \
			echo "Killing processes using ports 50050 or 50051: $$pids"; \
			kill -9 $$pids; \
		else \
			echo "No process using ports 50050 or 50051."; \
		fi \
	}