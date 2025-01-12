const frisby = require("frisby");
frisby.globalSetup({
  request: {
    headers: {
      "Content-Type": "application/json",
    },
  },
});

module.exports.frisby = frisby;
