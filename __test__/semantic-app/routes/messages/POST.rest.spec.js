describe("POST /api/messages", () => {
  const config = require("../../config/environment/local"),
  { v4: uuidv4 } = require("uuid");

  const frisby = config.frisby,
  schemas = {
    Response: require("../../models/Response.joi")
  }

  Object.entries(config.endpoints).forEach(([app_name, url]) => {
    describe(`${app_name}: ${url}`, () => {
      it(`should return a valid Response`, async () => {
        request = { id: uuidv4(), message: "hello" };

        return frisby
          .post(url, request, { json: true })
          .expect("status", 200)
          .expect("jsonTypes", "request", schemas.Response);
      });
    });
  });
});
