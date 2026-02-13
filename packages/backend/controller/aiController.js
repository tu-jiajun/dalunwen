const OpenAI = require("openai");

// Initialize OpenAI client with Aliyun endpoint
const openai = new OpenAI({
  apiKey: "sk-a5dd51f65116498ea6270abb19c4d979", // Ideally from env
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

async function generateProtocol(ctx) {
  try {
    const { messages } = ctx.request.body;

    if (!messages || !Array.isArray(messages)) {
      ctx.status = 400;
      ctx.body = { code: 400, msg: "Invalid messages format" };
      return;
    }

    const completion = await openai.chat.completions.create({
      model: "qwen-max", // Using qwen-max as seen in previous analysis files
      messages: messages,
    });

    const content = completion.choices[0].message.content;
    console.log("AI Generation Content:", content);

    ctx.status = 200;
    ctx.body = {
      code: 200,
      msg: "Success",
      data: content,
    };
  } catch (error) {
    console.error("AI Generation Error:", error);
    ctx.status = 500;
    ctx.body = {
      code: 500,
      msg: `Generation failed: ${error.message}`,
    };
  }
}

module.exports = {
  generateProtocol,
};
