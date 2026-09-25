from laya import Router


class DecisionEngine:

    def __init__(self):

        self.router = Router(
            preload=True
        )

    def analyze(self, message: str):

        state = {
            "body": message
        }

        questions = {

            "department": {
                "type": "choice",
                "instructions": (
                    "Which department should handle "
                    "this customer request?"
                ),
                "criteria": {
                    "billing": (
                        "payments, invoices, refunds, "
                        "duplicate charges"
                    ),
                    "technical": (
                        "bugs, errors, outages, "
                        "broken features"
                    ),
                    "sales": (
                        "pricing, plans, contracts, "
                        "purchasing"
                    ),
                    "general": (
                        "anything else"
                    ),
                },
            },

            "urgency": {
                "type": "score",
                "instructions": (
                    "How urgent is this customer request?"
                ),
                "criteria": [
                    "not urgent",
                    "needs attention soon",
                    "critical",
                ],
            },

            "needs_human": {
                "type": "noul",
                "instructions": (
                    "Does this request require human review?"
                ),
                "criteria": {
                    "true": (
                        "the request requires human review"
                    ),
                    "false": (
                        "the request can be handled automatically"
                    ),
                },
            },
        }

        result = self.router.predict(
            state,
            questions,
            model="typed-decisions",
        )

        answers = result["answers"]

        department = answers["department"]

        return {
            "department": department["choice"],
            "department_probability": (
                department["probabilities"][
                    department["choice"]
                ]
            ),
            "urgency": answers["urgency"]["score"],
            "human_probability": (
                answers["needs_human"]["noul"]
            ),
            "raw": result,
        }