import time
import random

from google.genai.errors import (
    ClientError,
    ServerError
)


class Retry:

    def __init__(
        self,
        retries=6,
        base_delay=5,
        max_delay=60
    ):

        self.retries = retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def run(self, func):

        delay = self.base_delay

        for attempt in range(
            1,
            self.retries + 1
        ):

            try:

                return func()

            except ClientError as e:

                status = getattr(
                    e,
                    "code",
                    None
                )

                if status != 429:

                    raise

                print(
                    f"\nRate limit reached."
                )

            except ServerError:

                print(
                    "\nGemini temporarily unavailable."
                )

            except Exception:

                if attempt == self.retries:

                    raise

            if attempt == self.retries:

                raise

            wait = min(
                delay,
                self.max_delay
            )

            wait += random.uniform(
                0,
                2
            )

            print(
                f"Retry {attempt}/{self.retries}"
            )

            print(
                f"Waiting {wait:.1f} seconds...\n"
            )

            time.sleep(wait)

            delay *= 2