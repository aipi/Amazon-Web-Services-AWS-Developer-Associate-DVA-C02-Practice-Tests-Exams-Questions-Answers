
### You are providing AWS consulting services for a company developing a new mobile application that will be leveraging Amazon SNS Mobile Push for push notifications. In order to send direct notification messages to individual devices each device registration identifier or token needs to be registered with SNS; however the developers are not sure of the best way to do this. You advise them to:

- [ ] Bulk upload the device tokens contained in a CSV file via the AWS Management Console.
- [ ] Let the push notification service (e.g. Amazon Device Messaging) handle the registration.
- [ ] Implement a token vending service to handle the registration.
- [x] Call the CreatePlatformEndPoint API function to register multiple device tokens.

### An application contains two components: one component to handle HTTP requests, and another component to handle background processing tasks. Each component must scale independently. The developer wants to deploy this application using AWS Elastic Beanstalk. How should this application be deployed, based on these requirements?

- [ ] Deploy the application in a single Elastic Beanstalk environment.
- [x] Deploy each component in a separate Elastic Beanstalk environment.
- [ ] Use multiple Elastic Beanstalk environments for the HTTP component but one environment for the background task component.
- [ ] Use multiple Elastic Beanstalk environments for the background task component but one environment for the HTTP component.
