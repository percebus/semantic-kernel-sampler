const { Joi } = require("frisby");
const schemas = {
  Post: require("./Post.joi"),
};

module.exports = {
  id: Joi.string().required(),
  text: Joi.string().required(),
  postId: schemas.Post.id,
};
