var https = require("https");
const fs = require("fs");
const argv = require("node:process");
const override = argv[2]

class photos {
    constructor(links){
        if (links.length > 0){
            this.full = links[0].full;}
    }
}
class dog {
    constructor(animal){
        this.breed1 = animal.breeds.primary;
        this.breed2 = animal.breeds.secondary;
        this.mixed = animal.breeds.mixed;
        this.age = animal.age;
        this.gender = animal.gender;
        this.size = animal.size;
        this.name = animal.name;
        this.desc = String(animal.description).replaceAll('&amp;#39;', "\'");
        this.apa_id = animal.organization_animal_id;
        this.url = "https://apamo.org/adopt/adoptable-pets/?petID=" + this.apa_id;
        this.photo = (new photos(animal.photos)).full;
        this.created_datetime = animal.published_at;
        this.lastmod_datetime = animal.status_changed_at;
        //this.status = animal.status;
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
    let dogs = [];
    let k9arr= [];
    earliest = await fetch('https://api.petfinder.com/v2/animals/?type=dog&status=adoptable&organization=MO228&limit=100&sort=recent', options)
    .then((response) => response.json())
    .then((body) => {
        body.animals.forEach(animal=> {
            if(animal.species.toLowerCase() == "dog"){
                k9 = new dog(animal);
                k9arr.push(k9);
                dogs.push(Object.values(k9));
                ids.push(animal.organization_animal_id);
            }
        });});
    latest = await fetch("https://api.petfinder.com/v2/animals/?type=dog&status=adoptable&organization=MO228&limit=100&sort=-recent", options)
    .then((response) => response.json())
    .then((body) => {
        body.animals.forEach(animal=> {
            if(animal.species.toLowerCase() == "dog" && !ids.includes(animal.organization_animal_id)){
                k9 = new dog(animal);
                k9arr.push(k9);
                dogs.push(Object.values(k9));
                ids.push(animal.organization_animal_id);
            }
        });});
    var file = fs.createWriteStream('dogData.csv');
    file.on('error', function(err) {console.log(err)});
    file.write("sep=;" + '\n');
    dogs.forEach(function(v) {file.write(v.join(';') + '\n');});
    file.end();
    //fs.writeFile("fstest.csv", dogs_buffer, (err) => {if (err) throw err;})
    const count = ids.length;
    if (count < 200 && override != "override"){
        console.log("There are " + count + " dogs in the shelter")
    } else {
        console.log("Capacity reached! See dogData.csv")
        }
    return k9arr
}
async function atRisk(dogs){
    riskList = dogs.filter((dog) => ((dog.age == "Adult"||dog.age == "Senior") && (dog.size == "Large"||dog.size == "Medium")));
    let riskArr = [];
    riskList.forEach(function(v){riskArr.push(Object.values(v));});
    var file = fs.createWriteStream('atRisk.csv');
    file.on('error', function(err) {console.log(err)});
    //file.write("sep=;" + '\n');
    try{
    riskArr.forEach(function(v) {file.write(v.join(';') + '\n');});
    file.end();}
    catch(error){
        console.log(error);
    }
}
async function main(){
    dogs = await buildDB();
    atRisk(dogs);
}
main()