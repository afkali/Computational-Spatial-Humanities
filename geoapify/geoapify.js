
//https://www.geoapify.com/solutions/batch-geocoding-requests/

//hier Daten eingeben
var data = [
    "London",
    "545 Southwest Taylor Street, Portland, OR 97204, United States of America",
    "1415 Southwest Park Avenue, Portland, OR 97201, United States of America"
];

// ca 3000 
const url = `https://api.geoapify.com/v1/batch/geocode/search?apiKey=887c2a05f4ba4a41aa08ce48fe5c1e6f`;


fetch("https://api.geoapify.com/v1/batch/geocode/search?apiKey=887c2a05f4ba4a41aa08ce48fe5c1e6f", {
    method: 'post',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)

})
    .then(getBodyAndStatus)
    .then((result) => {
        if (result.status !== 202) {
            return Promise.reject(result)
        } else {
            console.log("Job ID: " + result.body.id);
            console.log("Job URL: " + result.body.url)
            return getAsyncResult(`${url}&id=${result.body.id}`, 1000, 100).then(queryResult => {
                console.log(queryResult);
                queryResult.forEach(WriteToFile)
                return queryResult;
            });
        }
    })
    .catch(err => console.log(err));

function WriteToFile(item) {

    console.log(item.formatted.toString());
    const fs = require('fs')
    fs.appendFile('tp.txt', item.formatted.toString()+"\n", (err) => {
        if (err) throw err;
        else {
            console.log("The file is updated with the given data")
        }
    })
    fs.appendFile('tp.txt', item.lon.toString() + "\n", (err) => {
        if (err) throw err;
        else {
            console.log("The file is updated with the given data")
        }
    })
    fs.appendFile('tp.txt', item.lat.toString() + "\n", (err) => {
        if (err) throw err;
        else {
            console.log("The file is updated with the given data")
        }
    })
    console.log(item.lon);
    console.log(item.lat);

    
}

function getBodyAndStatus(response) {
    return response.json().then(responceBody => {
        return {
            status: response.status,
            body: responceBody
        }
    });
}

function getAsyncResult(url, timeout, maxAttempt) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            repeatUntilSuccess(resolve, reject, 0)
        }, timeout);
    });

    function repeatUntilSuccess(resolve, reject, attempt) {
        console.log("Attempt: " + attempt);
        fetch(url)
            .then(getBodyAndStatus)
            .then(result => {
                if (result.status === 200) {
                    resolve(result.body);
                } else if (attempt >= maxAttempt) {
                    reject("Max amount of attempt achived");
                } else if (result.status === 202) {
                    // Check again after timeout
                    setTimeout(() => {
                        repeatUntilSuccess(resolve, reject, attempt + 1)
                    }, timeout);
                } else {
                    // Something went wrong
                    reject(result.body)
                }
            })
            .catch(err => reject(err));
    };
}