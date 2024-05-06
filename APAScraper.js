var https = require("https");
const fs = require("fs");
const argv = require("node:process");
const id = "y1ojzoyO7TvfNHyXfWDZAX9rL1GUIrgbGOnqPvtzAs3FoC0S0O";
const secret = "rjK77I88buUdQmqhZ4tcc1HMOevOKgP7NdNM49Hf";
const override = argv[2]

class dog {
    constructor(animal){
        this.petfinder_id = animal.id;
        this.breed1 = animal.breeds.primary;
        this.breed2 = animal.breeds.secondary;
        this.mixed = animal.breeds.mixed;
        this.age = animal.age;
        this.gender = animal.gender;
        this.size = animal.size;
        this.name = animal.name;
        this.desc = "\"\"" + animal.description + "\"\"";
        this.apa_id = animal.organization_animal_id;
        this.url = "https://apamo.org/adopt/adoptable-pets/?petID=" + this.apa_id;
        this.photo = animal.photos.full;
        this.created_datetime = animal.published_at;
        this.lastmod_datetime = animal.status_changed_at;
        this.status = animal.status;
        }
}

async function getToken(){
    token = await fetch('https://api.petfinder.com/v2/oauth2/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'grant_type=client_credentials&client_id='+id+'&client_secret='+secret
    })
    .then((response) => response.json())
    .then((body) => (token = body.access_token));
    return token
}
async function buildDB(){
    const token = await getToken();
    ids = []
    const options = {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + token}
    };
    let dogs = [["Petfinder ID", "Primary Breed", "Secondary Breed", "Mixed?", "Age", "Gender", "Size", "Name", "Description", "APA ID", "URL", "Photo", "Created at", "Last Modified", "Status"]];
    earliest = await fetch('https://api.petfinder.com/v2/animals/?type=dog&status=adoptable&organization=MO228&limit=100&sort=recent', options)
    .then((response) => response.json())
    .then((body) => {
        body.animals.forEach(animal=> {
            if(animal.species.toLowerCase() == "dog"){
                k9 = new dog(animal);
                dogs.push(Object.values(k9));
                ids.push(animal.organization_animal_id);
            }
        });});
        //dogs needs to be converted to bytes/intarray
    latest = await fetch("https://api.petfinder.com/v2/animals/?type=dog&status=adoptable&organization=MO228&limit=100&sort=-recent", options)
    .then((response) => response.json())
    .then((body) => {
        body.animals.forEach(animal=> {
            if(animal.species.toLowerCase() == "dog" && !ids.includes(animal.organization_animal_id)){
                k9 = new dog(animal);
                dogs.push(Object.values(k9));
                ids.push(animal.organization_animal_id);
            }
        });});
    var file = fs.createWriteStream('dogData.csv');
    file.on('error', function(err) {console.log(err)});
    dogs.forEach(function(v) { file.write(v.join(', ') + '\n'); });
    file.end();
    //dogs_buffer = new ArrayBuffer[dogs];
    //fs.writeFile("fstest.csv", dogs_buffer, (err) => {if (err) throw err;})
    const count = ids.length;
    if (count < 200 && override != "override"){
        console.log("There are " + count + " dogs in the shelter")
    } else {
        console.log("Capacity reached! See dogData.csv")
        }
    
}
buildDB();