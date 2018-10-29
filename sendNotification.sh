curl -X POST --header "Authorization: key=" \
    --Header "Content-Type: application/json" \
    https://fcm.googleapis.com/fcm/send \
    -d "{\"to\":\"HERE DEST KEY\",\"notification\":{\"body\":\"Yellow\"},\"priority\":10}"