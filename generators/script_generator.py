from database.database_controller import DatabaseController
from llm.openai_wrapper import OpenAIWrapper
from prompt.script_generator_prompt_manager import ScriptGeneratorPromptManager
#from gpt4free import Provider, quora
import gpt4free


class ScriptGenerator:
    def __init__(self):
        self.database_controller = DatabaseController()
        self.script_generato_prompt_manager = ScriptGeneratorPromptManager()
        self.openai_wrapper = OpenAIWrapper()
        self.openai_fast_model = "gpt-3.5-turbo-0613"
        self.fast_token_limit = 1500
        self.use_openai = True

    def generate_script_options(self, script_generator_id:int, product_name, keywords_or_desc):
        recent_scripts = self.database_controller.get_recent_completed_scripts(script_generator_id)

        if self.use_openai:
            messages = self.script_generato_prompt_manager.create_script_generator_messages(
                recent_scripts=recent_scripts,
                target_product_name=product_name,
                target_keywords_desc=keywords_or_desc,
                influencer_name="yesstella")

            response = self.openai_wrapper.create_chat_completion(messages=messages, model=self.openai_fast_model,
                                                                  temperature=1, max_tokens=self.fast_token_limit)
            print(f"[ScriptGenerator.generate_script_options()] get_response_from_openai: {response}")
            return response

        else:
            prompt = self.script_generato_prompt_manager.create_script_generator_prompt(
                recent_scripts=recent_scripts,
                target_product_name=product_name,
                target_keywords_desc=keywords_or_desc,
                influencer_name="yesstella")

            response = ""

            token = quora.Account.create(logging=False)
            response = gpt4free.Completion.create(Provider.Poe, prompt=prompt, token=token,
                                                  model='ChatGPT')

            print(f"[ScriptGenerator.generate_script_options()] get_response_from_not_openai: {response}")
            return response




