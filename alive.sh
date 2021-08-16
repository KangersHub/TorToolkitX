while true
do
    sleep 25m # sleep NUMBER[SUFFIX]. SUFFIX= seconds (s), minutes (m), hours (h) and days (d). Given value 5 is 5 seconds.
    wget -q -O/dev/null $BASE_URL_OF_BOT
done
