# Ubuntu temporarily, for testing services
FROM ubuntu:latest

# Run apt-get install for the bot
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install iputils-ping -y
RUN pip3 install discord
RUN pip3 install requests
RUN pip3 install asyncio
RUN pip3 install "aiohttp>=3.6.1,<3.8.0"