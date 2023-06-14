from llm.base import Message

class ScriptGeneratorPromptManager:
    def __init__(self):
        with open('prompt_templates/script_generator_three_options_prompt_template.txt', 'r', encoding='utf-8') as file:
            self.script_generator_three_options_prompt_template = file.read()

    def create_script_generator_prompt(self, recent_scripts, target_product_name, target_keywords_desc,
                                       influencer_name):
        examples = ""
        for recent_script in recent_scripts:
            example = f"产品名：{recent_script['product_name']} \n关键词或描述：{recent_script['keywords_desc']}\n脚本：{recent_script['script']}\n"
            examples = examples + example

        content = self.script_generator_three_options_prompt_template.replace("${INFLUENCER_NAME}$", influencer_name)
        content = content.replace("${EXAMPLES}$", examples)
        content = content.replace("${TARGET_PRODUCT_NAME}$", target_product_name)
        content = content.replace("${TARGET_KEYWORDS_OR_DESCRIPTIONS}$", target_keywords_desc)

        return content

    def create_script_generator_messages(self, recent_scripts, target_product_name, target_keywords_desc,
                                         influencer_name):
        content = self.create_script_generator_prompt(recent_scripts, target_product_name, target_keywords_desc,
                                                      influencer_name)
        messages = []
        message = Message(role="user", content=content)
        messages.append(message)
        return messages
