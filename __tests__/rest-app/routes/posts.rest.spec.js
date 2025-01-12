describe("rest-app/", () => {
  const config = require("../config"),
    environment = require("../../config/environments/environment"),
    { v4: uuidv4 } = require("uuid");

  const frisby = config.frisby;
  const schemas = {
    Post: require("../models/Post.joi"),
  };

  describe("posts/", () => {
    const url = `${environment["rest-app"].url}/posts/`;
    describe("GET", () => {
      it("returns a list of posts", async () => {
        return frisby
          .get(url)
          .expect("status", 200)
          .expect("jsonTypes", "*", schemas.Post);
      });
    });
  });

  // FIXME
  xdescribe("posts/-1: PUT", () => {
    const postId = "-1";
    const url = `${environment["rest-app"].url}/posts/${postId}`;
    const newPost = { id: postId, title: "Some new TEST title", views: 0 };

    describe("GET 1", () => {
      it("returns the new Post", async () => {
        return frisby.get(url).expect("status", 404);
      });
    });

    describe("PUT", () => {
      it("returns puts a new Post", async () => {
        return frisby.put(url, newPost).expect("status", 200);
      });
    });

    describe("GET 2", () => {
      it("returns the new Post", async () => {
        return frisby
          .get(url)
          .expect("status", 200)
          .expect("jsonTypes", schemas.Post);
      });
    });

    describe("DELETE", () => {
      it("deletes the Post", async () => {
        return frisby.del(url).expect("status", 200);
      });
    });

    describe("GET 3", () => {
      it("returns the new Post", async () => {
        return frisby.get(url).expect("status", 404);
      });
    });
  });

  // XXX it modifies the db/blog.json
  // FIXME we should be using PUT, but it returns 404
  xdescribe("posts/: POST", () => {
    const url = `${environment["rest-app"].url}/posts/`;
    const newPost = { title: "Some new TEST title", views: 0 };

    describe("GET 1", () => {
      it("returns the new Post", async () => {
        return frisby
          .get(url)
          .expect("status", 200)
          .expect("jsonTypes", "*", schemas.Post);
      });
    });

    describe("POST", () => {
      it("returns puts a new Post", async () => {
        return frisby.post(url, newPost).expect("status", 201);
      });
    });

    describe("GET 2", () => {
      it("returns the new Post", async () => {
        return frisby
          .get(url)
          .expect("status", 200)
          .expect("jsonTypes", "*", schemas.Post);
      });
    });
  });
});
