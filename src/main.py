from config import config
from llm import ask_question, answer_question, choose_the_best_answer
from schemas import Answer, ModelRating
from typing import List
from collections import defaultdict
import asyncio
import logfire


def process_answers(answers: List[Answer]) -> List[ModelRating]:
    model_ratings = defaultdict(int)
    model_speeds = defaultdict(float)
    model_counts = defaultdict(int)
    for answer in answers:
        model_ratings[answer.model] += answer.rating
        model_speeds[answer.model] += answer.speed
        model_counts[answer.model] += 1
    return sorted(
        [ModelRating(model=model, rating=rating, total_speed=model_speeds[model], average_speed=model_speeds[model] / model_counts[model], answer_count=model_counts[model]) 
         for model, rating in model_ratings.items()],
        key=lambda x: (-x.rating, x.model) 
    )

def display_results(results: List[ModelRating]):
    print(f"\nIntended: {config.INTENDED}")
    print("\n" + "=" * 100)
    print(f"{'MODEL':<45} | {'RATING':<8} | {'AVG SPEED (s)':<12} | {'TOTAL SPEED (s)':<14} | {'ANSWERS':<7}")
    print("-" * 100)
        
    for result in results:
        print(f"{result.model:<45} | {result.rating:<8} | {result.average_speed:<12.2f} | {result.total_speed:<14.2f} | {result.answer_count:<7}")
    
    print("=" * 100)
    print(f"\nBest model: {results[0].model} with rating: {results[0].rating}")
    print("=" * 100)


async def main():
    try:
        logfire.info("Start")
        all_evaluations = []
        for i in range(config.NUMBER_OF_REPETITIONS):
            tasks = [ask_question(model) for model in config.MODELS]
            questions = await asyncio.gather(*tasks)
            questions = list(filter(None, questions))
            logfire.info("Questions",questions=questions)
            for q_model, question in zip(config.MODELS, questions):
                tasks = [answer_question(model, question) for model in config.MODELS]
                answers = await asyncio.gather(*tasks)
                answers = list(filter(None, answers))

                tasks = [choose_the_best_answer(model, question, answers) for model in config.MODELS]
                evaluated_answers = await asyncio.gather(*tasks)
                evaluated_answers = list(filter(None, evaluated_answers))
                flattened_answers = [item for sublist in evaluated_answers for item in sublist]

                logfire.info("Avaluated answers",evaluated_answers=flattened_answers)
                all_evaluations += flattened_answers
        
        logfire.info("All evaluations",evaluations=all_evaluations)
        print(all_evaluations)
        
        ans = process_answers(all_evaluations)
        logfire.info("Final assessment",ans=ans)
        display_results(ans)
        await asyncio.sleep(1)
        logfire.info("Stop")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
    