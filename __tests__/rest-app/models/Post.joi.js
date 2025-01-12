const { Joi } = require("frisby");

module.exports = {
    id: Joi.string().required(),
    title: Joi.string().required(),
    views: Joi.number().required()
};
