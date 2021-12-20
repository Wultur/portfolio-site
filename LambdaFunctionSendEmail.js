var AWS = require("aws-sdk");
var ses = new AWS.SES({ region: "us-east-1" });

var RECEIVER = "your@mail.com";
var SENDER = "your@mail.com";

exports.handler = async function (event) {
    console.log('Received event:', event);
    var params = {
        Destination: {
            ToAddresses: [RECEIVER]
        },
        Message: {
            Body: {
                Text: {
                    Data: 'Name: ' + event.name + '\nE-mail: ' + event.email + '\nDescription: ' + event.desc,
                    Charset: 'UTF-8'
                }
            },
            Subject: {
                Data: 'Contact Form: ' + event.name,
                Charset: 'UTF-8'
            }
        },
        Source: SENDER
    }
    return ses.sendEmail(params).promise();
};
