# Lightweight image for running the bot
# Note: Don't use alpine
FROM python:3.9-bullseye

# Copy requirements.txt to the image
ADD Build/requirements.txt /requirements.txt

# Install requirements
RUN pip3 install -r /requirements.txt

# Run apt-get install for the bot
RUN apt-get update
RUN apt-get install iputils-ping -y


# Copy the bot to the image
ADD bot.py /bot.py
ADD config.py /config.py
ADD secrets.py /secrets.py
# Copy the entire cogs directory to the image
ADD Cogs /Cogs

# Start the bot
RUN python3 /bot.py
