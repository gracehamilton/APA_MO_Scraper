const {SQLclient} = require('pg');
const ini = require('ini');
const fs = require('fs')

process = fs.readFile('config/requirements.ini', 'utf-8')
    .then((data) => {
        const creds = ini.parse(data);
        console.log(creds)
    }
    )
