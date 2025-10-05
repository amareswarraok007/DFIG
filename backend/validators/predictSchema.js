const Joi = require('joi');

const schema = Joi.object({
  N: Joi.number().required(),
  P: Joi.number().required(),
  K: Joi.number().required(),
  temperature: Joi.number().required(),
  humidity: Joi.number().required(),
  ph: Joi.number().required(),
  rainfall: Joi.number().required()
}).unknown(false);

module.exports = (payload) => schema.validate(payload);
