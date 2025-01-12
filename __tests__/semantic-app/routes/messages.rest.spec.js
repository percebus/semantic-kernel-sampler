describe("semantic-app/", () => {
  describe("POST api/messages", () => {
    const config = require("../config"),
      environment = require("../../config/environments/environment"),
      { v4: uuidv4 } = require("uuid");

    const frisby = config.frisby,
      schemas = {
        Response: require("../models/Response.joi"),
      };

    Object.entries(environment["semantic-app"]).forEach(([app_name, url]) => {
      describe(`${app_name} @ ${url}`, () => {
        describe("{id:UUID, message:'hello'}", () => {
          it(`should return a valid Response`, async () => {
            request = { id: uuidv4(), message: "hello" };

            return frisby
              .post(url, request, { json: true })
              .expect("status", 200)
              .expect("jsonTypes", schemas.Response);
          });
        });

        describe("{message:'hello'}", () => {
          it(`should return a valid Response`, async () => {
            request = { message: "hello" };

            return frisby
              .post(url, request, { json: true })
              .expect("status", 200)
              .expect("jsonTypes", schemas.Response);
          });
        });
      });
    });
  });
});
