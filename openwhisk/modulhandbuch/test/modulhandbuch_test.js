/**
 * Created by Armin on 05.06.2017.
 */
var request = require('request');
var actionUrl = 'https://service.us.apiconnect.ibmcloud.com/gws/apigateway/api/'+process.env.WSK_API_CODE+'/iwibotTest/semester';
var params = {
    context: {
        semester: 1,
        courseOfStudies: 'INFB'
    }
};

module.exports = {
    'Semester Action Test' : function (test) {
        test.expect(2);
        request.post({
            headers: {'content-type': 'application/json'},
            url: actionUrl,
            body: JSON.stringify(params)
        }, function (err, response, body) {
            console.log('\n Action URL: \n' + actionUrl);
            console.log('\n Body:       \n' + JSON.stringify(body, null, 4));
            console.log('\n Error:      \n' + err);
            console.log('\n Response:   \n' + JSON.stringify(response, null, 4));
            //body = JSON.parse(body);
            test.ok(response.statusCode == 204 || response.statusCode == 200);
            //test.ok(body.payload.indexOf('Es ist ein Fehler beim anmelden passiert.') == -1);
            test.ok(!err);
            test.done();
        });
    }
};