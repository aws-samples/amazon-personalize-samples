const AWS = require('aws-sdk')
var personalizeevents = new AWS.PersonalizeEvents();
var dynamoClient = new AWS.DynamoDB.DocumentClient();

console.log('Loading function');

exports.handler = (event, context, callback) => {
    console.log(JSON.stringify(event, null, 2));
    
    event.Records.forEach(function(record) {
        // Kinesis data is base64 encoded so decode here
        var payload = Buffer.from(record.kinesis.data, 'base64').toString('ascii');
        console.log('Decoded payload:', payload);
        payload = JSON.parse(payload);
        var eventDate = new Date();
        var putEventsParams= {
            'sessionId': payload.SessionId, /* required */
            'trackingId': process.env.TRACKING_ID, /* required */
            'userId': payload.UserId,
            eventList: [
                {
                  'eventType': payload.EventType, /* required */
                  'properties': payload.Event, /* required */
                  'sentAt': eventDate
                },
            ]
        }
        console.log("THIS IS THE OBJECT = " + JSON.stringify(putEventsParams,null,3))
        personalizeevents.putEvents(putEventsParams, function (err, data) {
          if (err) {
                console.log(err, err.stack); // an error occurred
          }
          else{     
                console.log(data);           // successful response
                putEventsParams['eventList'][0]['sentAt']=putEventsParams['eventList'][0]['sentAt'].toTimeString();
                const putEventsErrResponse = {
                    statusCode: 500,
                    body: JSON.stringify(err),
                };
                callback(null, putEventsErrResponse);
                const response = {
                    statusCode: 200,
                    body: JSON.stringify(putEventsParams),
                };
                callback(null, response);
          }
        });
    });
};