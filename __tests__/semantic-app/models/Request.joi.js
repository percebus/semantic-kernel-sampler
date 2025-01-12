const { Joi } = require("frisby");

module.exports = {
  id: Joi.string().required(),
  message: Joi.string().required(),
};
