const OpenAI = require("openai");
const { ALI_LLM_CONFIG } = require("../config/aiConfig");

const aiClient = new OpenAI({
  apiKey: ALI_LLM_CONFIG.API_KEY,
  baseURL: ALI_LLM_CONFIG.BASE_URL,
});

module.exports = aiClient;
