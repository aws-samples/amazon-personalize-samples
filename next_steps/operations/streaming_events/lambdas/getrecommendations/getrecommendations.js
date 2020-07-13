const AWS = require('aws-sdk')
var personalizeruntime = new AWS.PersonalizeRuntime();
var dynamoClient = new AWS.DynamoDB.DocumentClient();


exports.handler = (event, context, callback) => {
    
    console.log(JSON.stringify(event,null,3))

    // We are getting the user ID from the query string parameters
    var userId= event.queryStringParameters.userId;
    
    var params = {
        campaignArn: process.env.CAMPAIGN_ARN, /* required */
        // userId: body.userId
        userId: userId
    };
    personalizeruntime.getRecommendations(params, function(personalizeErr, personalizeData) {
        if (personalizeErr) {
            console.log(personalizeErr, personalizeErr.stack); // an error occurred
            const personalizeRrrResponse = {
                statusCode: 500,
                body: JSON.stringify(personalizeErr),
            };
            callback(null, personalizeRrrResponse);
        }
        else  {
            // Logging the reply from Personalize 
            console.log(personalizeData);           // successful response
            // Let's write these recommendations to DynamoDB
            var currentDate = new Date();
            var params = {
              TableName: process.env.DDB_TABLE,
              Item:{
                userId: userId,
                timeStamp: currentDate.toTimeString(),
                recommendations: personalizeData
                  
              }
            };
            dynamoClient.put(params, function(dynamoErr, dynamoData) {
               if (dynamoErr){
                   console.log(dynamoErr);
                   const dynamoErrResponse = {
                        statusCode: 500,
                        body: JSON.stringify(dynamoErr),
                    };
                    callback(null, dynamoErrResponse);
               }
               else {
                   console.log(dynamoData);
                   const response = {
                        statusCode: 200,
                        body: JSON.stringify(personalizeData),
                    };
                    callback(null, response);
               }
            });
        }  
    });
};