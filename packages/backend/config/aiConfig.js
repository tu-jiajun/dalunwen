const ALI_LLM_CONFIG = {
  API_KEY:
    process.env.ALI_LLM_API_KEY ||
    process.env.DASHSCOPE_API_KEY ||
    process.env.OPENAI_API_KEY ||
    process.env.OPENAI_KEY ||
    "",
  BASE_URL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  MODEL: "qwen-max"
};

module.exports = {
  ALI_LLM_CONFIG
};
