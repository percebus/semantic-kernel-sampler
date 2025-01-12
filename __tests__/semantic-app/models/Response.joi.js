const { Joi } = require("frisby");

Request = require("./Request.joi");

module.exports = {
  request: Joi.object(Request).required(),
  id: Joi.string().required(),
  message: Joi.string().optional(),
};
