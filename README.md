# web-scraping

#Driver

docker pull selenium/standalone-chrome

#correr Driver

docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest
