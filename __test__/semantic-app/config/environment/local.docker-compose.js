const settings = require("../settings");
module.exports = settings;

module.exports.endpoints = {
    python: "http://127.0.0.1:8082/messages",
    dotnet: "http://127.0.0.1:8083/api/messages"
}
