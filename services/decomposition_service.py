import openai

from repositories.plan_repository import PlanRepository


class DecompositionService:
    def __init__(self, db):
        self.plan_repo = PlanRepository(db)

    def decompose_task(self, task_description, plan_id, min_points=6, max_points=10):
        try:
            # openai.api_key = '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'

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"Decompose the task '{task_description}' into {min_points} to {max_points} steps. "
                    }
                ]
            )

            message = response['choices'][0]['message']['content']
            steps = message.strip().split('\n')

            decomposition_text = "\n".join(steps)

            updated_plan = self.plan_repo.update_plan_decomposition(plan_id, decomposition_text)

            if not updated_plan:
                return [], f"Plan with ID {plan_id} not found."

            plan_data = {
                "planId": updated_plan.plan_id,
                "userId": updated_plan.user_id,
                "status": updated_plan.status,
                "name": updated_plan.name,
                "description": updated_plan.description,
                "duration": updated_plan.duration,
                "priority": updated_plan.priority,
                "deadline": updated_plan.deadline,
                "dayOfWeek": updated_plan.day_of_week,
                "decomposition": updated_plan.decomposition
            }

            return plan_data, None

        except Exception as e:
            return [], str(e)
