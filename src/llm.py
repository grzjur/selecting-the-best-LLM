from pydantic_ai import Agent
from config import config
from utils import extract_between_tags
from typing import List
from schemas import Answer
import time

system_prompt_ask = f"""
You are a helpful assistant testing LLM models, explains your reasoning step by step, incorporating dynamic Chain of Thought (CoT), reflection.

Tested LLM intended for: {config.INTENDED}

Your task is to create a question
Create a question you want to ask the LLM model, be creative.
Put the question in a <question> tag.

- at the beginning, attach all thoughts within <thinking> tags, exploring multiple angles and approaches.
- Use thoughts to reflect on the question.
- Remember to include the question between tags <question>...</question>

"""
async def ask_question(model):
    try:
        agentAsk = Agent(
            model=config.get_model(model),
            system_prompt=system_prompt_ask
        )
        result = await agentAsk.run("Create a question. Remember to include the question between tags <question>...</question>")
        question = extract_between_tags(result.data, "<question>", "</question>")
        return question
    except Exception as e:
        print(e)
        return ""


system_prompt_answer = """
You are a helpful assistant, explains your reasoning step by step, incorporating dynamic Chain of Thought (CoT), reflection.

You are answering a question asked by a user

- At the beginning, attach all thoughts within <thinking> tags, exploring multiple angles and approaches.
- Use thoughts to reflect on the answer.
- Put the answer in a <answer> tag.

"""
async def answer_question(model, question):
    try:
        agentAnswer = Agent(
            model=config.get_model(model),
            system_prompt=system_prompt_answer
        )
        start = time.time()
        result = await agentAnswer.run(question)
        end = time.time()
        answer = extract_between_tags(result.data, "<answer>", "</answer>")
        return Answer(model=model, question=question, answer=answer, speed=end-start)
    except Exception as e:
        print(e)
        return None

# evaluate
def get_system_prompt_rating(question):
    return f"""
You are an expert evaluator of responses, explains your reasoning step by step, incorporating dynamic Chain of Thought (CoT), reflection.

Your task is to choose the best answer. You can choose only one answer

- At the beginning, attach all thoughts within <thinking> tags, exploring multiple angles and approaches.
- Focus ONLY on choosing the best answer, not the question
- The question is included in the <question> tag
- Answers are included in <answer_n> tags
- Give your choice in <the_best> tag
- Be consistent in your evaluations 

<example>
User:
<question>how much is 2 + 3</question>
<answer_1>I don't know<answer_1>
<answer_2>2 + 3 = 5<answer_2>
<answer_3>something around 5<answer_3>

Model:
 <thinking>the best is answer no. 2, it is correct, complete. Other answers are not as good</thinking>
<the_best>2</the_best>
</example>

<question>
{question}
</question>

"""

async def choose_the_best_answer(model: str, question: str, answers: List[Answer]) -> List[Answer] | None:
    try:
        agentRate = Agent(
            model=config.get_model(model),
            system_prompt=get_system_prompt_rating(question)
        )

        user_prompt = '\n\n'.join([f"<answer_{i+1}>{item.answer}</answer_{i+1}>" for i, item in enumerate(answers)])
        result = await agentRate.run(user_prompt) 
        best_str = extract_between_tags(result.data, "<the_best>", "</the_best>")
        if best_str.isdigit():
            best = int(best_str)
            if 0 < best <= len(answers):
                answers[best-1].rating = 1
                return answers

        return None
    except Exception as e:
        print(e)
        return None
