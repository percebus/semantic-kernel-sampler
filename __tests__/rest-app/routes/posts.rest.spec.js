describe('rest-app', () => {
    const config = require('../config'),
    environment = require('../../config/environments/environment'),
    { v4: uuidv4 } = require('uuid');

    const frisby = config.frisby;
    const schemas = {
        Post: require('../models/Post.joi'),
    }

    describe('posts/', () => {
        const url = `${environment['rest-app'].url}/posts/`;
        describe('GET', () => {
            it("returns a list of posts", async () => {
                return frisby
                    .get(url)
                    .expect("status", 200)
                    .expect("jsonTypes", "*", schemas.Post);
            });
        });
    });
});
